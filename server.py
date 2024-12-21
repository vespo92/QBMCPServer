import json
import sys
import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from api import QuickBooksTimeAPI
from utils import setup_logging, log_info, log_error

JSONRPC_VERSION = "2.0"
PROTOCOL_VERSION = "2024-11-05"

SERVER_INFO = {
    "name": "qb-time-tools",
    "version": "1.0.0",
    "vendor": "QuickBooks Time API Client",
    "description": "Access QuickBooks Time data through these API tools.",
    "tools": [
        {
            "name": "get_jobcodes",
            "description": "Get all jobcodes from QuickBooks Time. Returns jobcode details including name, type, and status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {"type": "array", "items": {"type": "number"}, "description": "Filter by specific jobcode IDs"},
                    "parent_ids": {"type": "array", "items": {"type": "number"}, "description": "Filter by parent jobcode IDs"},
                    "name": {"type": "string", "description": "Filter by name (use * as wildcard)"},
                    "type": {"type": "string", "enum": ["regular", "pto", "paid_break", "unpaid_break", "all"]},
                    "active": {"type": "string", "enum": ["yes", "no", "both"]},
                    "customfields": {"type": "boolean"},
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "supplemental_data": {"type": "string", "enum": ["yes", "no"]},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_jobcode",
            "description": "Get details for a specific jobcode by ID.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "The ID of the jobcode to retrieve"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "search_jobcodes",
            "description": "Search jobcodes with advanced filtering options.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Search by name (use * as wildcard)"},
                    "type": {"type": "string", "enum": ["regular", "pto", "paid_break", "unpaid_break", "all"]},
                    "active": {"type": "string", "enum": ["yes", "no", "both"]},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_jobcode_hierarchy",
            "description": "Get complete jobcode hierarchy starting from top-level jobcodes.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Filter by name (use * as wildcard)"},
                    "type": {"type": "string", "enum": ["regular", "pto", "paid_break", "unpaid_break", "all"]},
                    "active": {"type": "string", "enum": ["yes", "no", "both"]},
                    "customfields": {"type": "boolean"},
                    "supplemental_data": {"type": "string", "enum": ["yes", "no"]}
                }
            }
        },
        {
            "name": "get_timesheets",
            "description": "Get timesheets from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_timesheet",
            "description": "Get a specific timesheet by ID.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "The ID of the timesheet to retrieve"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_current_timesheets",
            "description": "Get currently active timesheets.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_users",
            "description": "Get users from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_user",
            "description": "Get a specific user by ID.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "The ID of the user to retrieve"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_current_user",
            "description": "Get details about the currently authenticated user.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_groups",
            "description": "Get groups from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_custom_fields",
            "description": "Get custom tracking fields configured on timecards.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_projects",
            "description": "Get projects from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_project_activities",
            "description": "Get project activities.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_last_modified",
            "description": "Get last modified timestamps for objects.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "types": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        {
            "name": "get_notifications",
            "description": "Get notifications.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_managed_clients",
            "description": "Get managed clients.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_current_totals",
            "description": "Get current totals snapshot including shift and day totals.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_payroll",
            "description": "Get payroll report.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                },
                "required": ["start_date", "end_date"]
            }
        },
        {
            "name": "get_payroll_by_jobcode",
            "description": "Get payroll report grouped by jobcode.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                },
                "required": ["start_date", "end_date"]
            }
        },
        {
            "name": "get_project_report",
            "description": "Get detailed project report with time entries.",
            "inputSchema": {
                "type": "object",
                "required": ["start_date", "end_date", "jobcode_ids"],
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format"
                    },
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by specific user IDs"
                    },
                    "group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by specific group IDs"
                    },
                    "jobcode_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by specific jobcode IDs (required)"
                    },
                    "jobcode_type": {
                        "type": "string",
                        "enum": ["regular", "pto", "unpaid_break", "paid_break", "all"],
                        "description": "Filter by jobcode type"
                    },
                    "customfielditems": {
                        "type": "object",
                        "description": "Filter by custom field items"
                    }
                }
            }
        }
    ]
}

class JSONRPCServer:
    def __init__(self, access_token: str, node_env: str):
        self.api = QuickBooksTimeAPI(access_token)
        self.node_env = node_env
        self.message_buffer = ''
        self.message_counter = 0
        setup_logging()

    def get_next_id(self) -> str:
        self.message_counter += 1
        return str(self.message_counter)

    def send_response(self, response: dict):
        response_str = json.dumps(response)
        sys.stdout.write(response_str + '\n')
        sys.stdout.flush()

    def send_error_response(self, id: str, code: int, message: str, data=None):
        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': id,
            'error': {
                'code': code,
                'message': message,
                'data': data
            }
        })

    def handle_initialize(self, message: dict):
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Initialize must include an id')
            return

        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': message['id'],
            'result': {
                'protocolVersion': PROTOCOL_VERSION,
                'capabilities': {
                    'tools': {
                        'listChanged': True
                    }
                },
                'serverInfo': SERVER_INFO
            }
        })

    def handle_tools_list(self, message: dict):
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Tools list request must include an id')
            return

        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': message['id'],
            'result': {
                'tools': SERVER_INFO['tools']
            }
        })

    def handle_tools_call(self, message: dict):
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Tools call must include an id')
            return

        params = message.get('params', {})
        name = params.get('name')
        args = params.get('arguments', {})

        if not name or not isinstance(args, dict):
            self.send_error_response(message['id'], -32602, 'Invalid params: must include name and arguments')
            return

        method_map = {
            'get_jobcodes': self.api.get_jobcodes,
            'get_jobcode': self.api.get_jobcode,
            'search_jobcodes': self.api.search_jobcodes,
            'get_jobcode_hierarchy': self.api.get_jobcode_hierarchy,
            'get_timesheets': self.api.get_timesheets,
            'get_timesheet': self.api.get_timesheet,
            'get_current_timesheets': self.api.get_current_timesheets,
            'get_users': self.api.get_users,
            'get_user': self.api.get_user,
            'get_current_user': self.api.get_current_user,
            'get_groups': self.api.get_groups,
            'get_custom_fields': self.api.get_custom_fields,
            'get_projects': self.api.get_projects,
            'get_project_activities': self.api.get_project_activities,
            'get_last_modified': self.api.get_last_modified,
            'get_notifications': self.api.get_notifications,
            'get_managed_clients': self.api.get_managed_clients,
            'get_current_totals': self.api.get_current_totals,
            'get_payroll': self.api.get_payroll,
            'get_payroll_by_jobcode': self.api.get_payroll_by_jobcode,
            'get_project_report': self.api.get_project_report
        }

        if name not in method_map:
            self.send_error_response(message['id'], -32601, f'Unknown method: {name}')
            return

        try:
            result = method_map[name](args)
            self.send_response({
                'jsonrpc': JSONRPC_VERSION,
                'id': message['id'],
                'result': {
                    'content': [{
                        'type': 'text',
                        'text': json.dumps(result)
                    }]
                }
            })
        except Exception as e:
            log_error(f'Error in {name}: {str(e)}')
            self.send_error_response(message['id'], -32000, str(e))

    def handle_message(self, message_str: str):
        message_id = self.get_next_id()

        try:
            message = json.loads(message_str)

            if 'method' not in message:
                self.send_error_response(
                    message.get('id', message_id),
                    -32600,
                    'Invalid Request'
                )
                return

            if message['method'] == 'initialize':
                self.handle_initialize(message)
            elif message['method'] == 'tools/list':
                self.handle_tools_list(message)
            elif message['method'] == 'tools/call':
                self.handle_tools_call(message)
            else:
                if 'id' in message:
                    self.send_error_response(message['id'], -32601, 'Method not found')
                else:
                    log_info(f'Received notification for method: {message["method"]}')

        except json.JSONDecodeError:
            self.send_error_response(message_id, -32700, 'Parse error')

    def send_server_info(self):
        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'method': 'server/info',
            'params': {
                'serverInfo': SERVER_INFO
            }
        })

    def start(self):
        log_info('QuickBooks Time MCP Server Starting')
        log_info(f'Environment: {{"tokenConfigured": {bool(self.api.access_token)}, "nodeEnv": "{self.node_env}"}}')

        # Send initial server info
        self.send_server_info()

        # Start reading from stdin
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                self.handle_message(line.strip())
            except KeyboardInterrupt:
                log_info('Server shutting down.')
                break

def run_server(access_token: str, node_env: str = 'development'):
    server = JSONRPCServer(access_token, node_env)
    server.start()

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    access_token = os.getenv('QB_TIME_ACCESS_TOKEN')
    node_env = os.getenv('NODE_ENV', 'development')

    if not access_token:
        print("QB_TIME_ACCESS_TOKEN environment variable is required")
        sys.exit(1)

    run_server(access_token, node_env)
