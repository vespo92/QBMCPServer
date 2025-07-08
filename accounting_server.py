"""
Enhanced QuickBooks Time MCP Server with accountant-friendly features
"""

import json
from typing import Dict, Any, Optional
from server import JSONRPCServer
from accounting_helpers import AccountingHelpers, PayrollWorkflows, InvoiceWorkflows
from utils import log_info, log_error

class AccountingFriendlyServer(JSONRPCServer):
    """Extended server with natural language processing and accounting workflows"""
    
    def __init__(self, access_token: str, node_env: str):
        super().__init__(access_token, node_env)
        self.helpers = AccountingHelpers()
        self.payroll_workflows = PayrollWorkflows()
        self.invoice_workflows = InvoiceWorkflows()
    
    def handle_tools_call(self, message: dict):
        """Override to add natural language processing and friendly responses"""
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Tools call must include an id')
            return

        params = message.get('params', {})
        name = params.get('name')
        args = params.get('arguments', {})

        if not name or not isinstance(args, dict):
            self.send_error_response(message['id'], -32602, 'Invalid params: must include name and arguments')
            return

        try:
            # Pre-process arguments for natural language dates
            processed_args = self._process_natural_language_args(args)
            
            # Add helpful context based on the operation
            context = self._get_operation_context(name, processed_args)
            
            # Call the original method
            method_map = {
                'get_jobcodes': self.api.get_jobcodes,
                'get_jobcode': self.api.get_jobcode,
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
                'get_project_report': self.api.get_project_report,
                # Add accounting-specific workflows
                'prepare_biweekly_payroll': self._prepare_biweekly_payroll,
                'month_end_closing': self._month_end_closing,
                'quarterly_tax_prep': self._quarterly_tax_prep,
                'prepare_client_invoice': self._prepare_client_invoice,
                'analyze_project_profitability': self._analyze_project_profitability,
            }

            if name not in method_map:
                # Try to suggest the right method
                suggestion = self._suggest_method(name)
                self.send_error_response(
                    message['id'], 
                    -32601, 
                    f'Unknown method: {name}. {suggestion}'
                )
                return

            result = method_map[name](processed_args)
            
            # Post-process the result to make it more accountant-friendly
            formatted_result = self._format_accounting_result(name, result, context)
            
            self.send_response({
                'jsonrpc': '2.0',
                'id': message['id'],
                'result': {
                    'content': [{
                        'type': 'text',
                        'text': json.dumps(formatted_result, indent=2)
                    }]
                }
            })
            
        except Exception as e:
            log_error(f'Error in {name}: {str(e)}')
            friendly_error = self.helpers.generate_friendly_error(str(e))
            self.send_error_response(message['id'], -32000, friendly_error)
    
    def _process_natural_language_args(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Convert natural language arguments to API format"""
        processed = args.copy()
        
        # Process date fields
        date_fields = ['start_date', 'end_date', 'modified_before', 'modified_since']
        for field in date_fields:
            if field in processed and isinstance(processed[field], str):
                processed[field] = self.helpers.parse_natural_date(processed[field])
        
        # Process terminology
        if 'type' in processed:
            processed['type'] = self.helpers.translate_accounting_terms(processed['type'])
        
        if 'jobcode_type' in processed:
            processed['jobcode_type'] = self.helpers.translate_accounting_terms(processed['jobcode_type'])
        
        return processed
    
    def _get_operation_context(self, operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get contextual information for the operation"""
        context = {
            'operation': operation,
            'purpose': 'general'
        }
        
        # Determine the purpose based on operation
        if 'payroll' in operation:
            context['purpose'] = 'payroll'
        elif 'project' in operation or 'jobcode' in operation:
            context['purpose'] = 'invoice'
        elif 'timesheet' in operation:
            context['purpose'] = 'timesheet'
        elif 'pto' in str(args.get('type', '')):
            context['purpose'] = 'pto'
        
        # Add date context
        if 'start_date' in args and 'end_date' in args:
            context['period'] = f"{args['start_date']} to {args['end_date']}"
        
        return context
    
    def _format_accounting_result(self, operation: str, result: Dict[str, Any], 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Format API results in accountant-friendly way"""
        formatted = {
            'summary': self.helpers.create_summary_header(
                context.get('purpose', 'general'),
                context.get('period', 'All Time').split(' to ')[0],
                context.get('period', 'Current').split(' to ')[-1]
            ),
            'data': result
        }
        
        # Add helpful formatting for specific operations
        if 'payroll' in operation and 'results' in result:
            formatted['formatted_totals'] = self._format_payroll_totals(result['results'])
        
        if 'timesheet' in operation and 'results' in result:
            formatted['formatted_entries'] = self._format_timesheet_entries(result['results'])
        
        # Add next action suggestions
        formatted['next_actions'] = self.helpers.suggest_next_action(context.get('purpose', ''))
        
        return formatted
    
    def _format_payroll_totals(self, payroll_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format payroll data in accounting-friendly format"""
        formatted = {}
        
        if 'payroll_report' in payroll_data:
            report = payroll_data['payroll_report']
            
            # Format overall totals
            if 'totals' in report:
                totals = report['totals']
                formatted['summary'] = {
                    'Regular Hours': self.helpers.format_seconds_to_hours(totals.get('total_re_seconds', 0)),
                    'Overtime Hours': self.helpers.format_seconds_to_hours(totals.get('total_ot_seconds', 0)),
                    'Double Time Hours': self.helpers.format_seconds_to_hours(totals.get('total_dt_seconds', 0)),
                    'PTO Hours': self.helpers.format_seconds_to_hours(totals.get('total_pto_seconds', 0)),
                    'Total Hours': self.helpers.format_seconds_to_hours(totals.get('total_work_seconds', 0))
                }
        
        return formatted
    
    def _format_timesheet_entries(self, timesheet_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format timesheet entries in accounting-friendly format"""
        formatted = []
        
        if 'timesheets' in timesheet_data:
            for ts_id, ts_data in timesheet_data['timesheets'].items():
                entry = {
                    'Employee': 'Unknown',  # Will be filled from supplemental data
                    'Date': ts_data.get('date', 'Unknown'),
                    'Hours': self.helpers.format_seconds_to_hours(ts_data.get('duration', 0)),
                    'Project': 'Unknown',  # Will be filled from supplemental data
                    'Notes': ts_data.get('notes', '')
                }
                
                # Add employee name from supplemental data
                if 'supplemental_data' in timesheet_data and 'users' in timesheet_data['supplemental_data']:
                    user_id = str(ts_data.get('user_id'))
                    if user_id in timesheet_data['supplemental_data']['users']:
                        user = timesheet_data['supplemental_data']['users'][user_id]
                        entry['Employee'] = f"{user.get('first_name', '')} {user.get('last_name', '')}"
                
                formatted.append(entry)
        
        return formatted
    
    def _suggest_method(self, attempted_method: str) -> str:
        """Suggest the correct method based on what was attempted"""
        suggestions = {
            'payroll': 'Did you mean "get_payroll" or "prepare_biweekly_payroll"?',
            'invoice': 'Did you mean "prepare_client_invoice" or "get_project_report"?',
            'hours': 'Did you mean "get_timesheets" or "get_current_totals"?',
            'employee': 'Did you mean "get_users" or "get_user"?',
            'client': 'Did you mean "get_projects" or "get_managed_clients"?',
            'pto': 'Did you mean "get_timesheets" with type="pto"?',
            'vacation': 'Did you mean "get_timesheets" with type="pto"?',
        }
        
        for key, suggestion in suggestions.items():
            if key in attempted_method.lower():
                return suggestion
        
        return 'Please check the available methods in the documentation.'
    
    # Accounting workflow methods
    def _prepare_biweekly_payroll(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare complete bi-weekly payroll"""
        end_date = args.get('end_date')
        workflow = self.payroll_workflows.prepare_biweekly_payroll(self.api, end_date)
        
        # Get actual payroll data
        start_date, end_date = workflow['period'].split(' to ')
        payroll_data = self.api.get_payroll({'start_date': start_date, 'end_date': end_date})
        
        # Combine workflow info with actual data
        return {
            'workflow': workflow,
            'payroll_data': payroll_data,
            'formatted_summary': self._format_payroll_totals(payroll_data.get('results', {}))
        }
    
    def _month_end_closing(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Run month-end closing process"""
        month = args.get('month')
        year = args.get('year')
        return self.payroll_workflows.month_end_closing(self.api, month, year)
    
    def _quarterly_tax_prep(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare quarterly tax data"""
        quarter = args.get('quarter')
        year = args.get('year')
        return self.payroll_workflows.quarterly_tax_prep(self.api, quarter, year)
    
    def _prepare_client_invoice(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare client invoice"""
        client_name = args.get('client_name')
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        hourly_rate = args.get('hourly_rate')
        
        workflow = self.invoice_workflows.prepare_client_invoice(
            self.api, client_name, start_date, end_date, hourly_rate
        )
        
        # Get actual project data
        project_data = self.api.get_project_report({
            'start_date': start_date,
            'end_date': end_date
        })
        
        return {
            'workflow': workflow,
            'project_data': project_data
        }
    
    def _analyze_project_profitability(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project profitability"""
        project_name = args.get('project_name')
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        
        return self.invoice_workflows.analyze_project_profitability(
            self.api, project_name, start_date, end_date
        )


def run_accounting_server(access_token: str, node_env: str = 'development'):
    """Run the enhanced accounting-friendly server"""
    server = AccountingFriendlyServer(access_token, node_env)
    server.start()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    access_token = os.getenv('QB_TIME_ACCESS_TOKEN')
    node_env = os.getenv('NODE_ENV', 'development')

    if not access_token:
        print("QB_TIME_ACCESS_TOKEN environment variable is required")
        import sys
        sys.exit(1)

    run_accounting_server(access_token, node_env)