# QuickBooks Time MCP Server (Combined)

This is a combined MCP server that provides access to all QuickBooks Time API functionality through a single interface. It combines the functionality of four separate servers:

1. JobCode Tools
2. Reports & Core Tools
3. Timesheet Tools
4. User Tools

I would LOVE help improving this project! Just glad to be able to give something back finally!

This entire project was developed and published using artificial intelligence (Anthropic, OpenAI, Llama/META), as I personally cannot write much code without assistance. While every effort has been made to ensure quality and functionality, there may be imperfections or areas for improvement. I welcome any feedback, corrections, or suggestions from the community.

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your QuickBooks Time access token:
```
QB_TIME_ACCESS_TOKEN=your_access_token_here
NODE_ENV=development
```

## Claude Desktop Configuration

To use this server with Claude Desktop, you'll need to configure it in your Claude Desktop settings. Here's an example configuration:

```json
{
  "globalShortcut": "Ctrl+Q",
  "mcpServers": {
    "qb-time-tools": {
      "command": "python",
      "args": [
        "./qb-time-mcp-server/main.py"
      ],
      "env": {
        "QB_TIME_ACCESS_TOKEN": "your_quickbooks_time_access_token_here"
      }
    }
  }
}
```

## Available Tools

### JobCode Tools
- `get_jobcodes`: Get jobcodes with advanced filtering options
  - Parameters:
    - `ids`: (array of numbers) Filter by specific jobcode IDs
    - `parent_ids`: (array of numbers) Filter by parent jobcode IDs
    - `name`: (string) Filter by name (use * as wildcard)
    - `type`: (string) Filter by type: "regular", "pto", "paid_break", "unpaid_break", "all"
    - `active`: (string) Filter by status: "yes", "no", "both"
    - `customfields`: (boolean) Include custom field data
    - `modified_before`: (string) Return items modified before this date
    - `modified_since`: (string) Return items modified after this date
    - `supplemental_data`: (string) Include supplemental data: "yes", "no"
    - `page`: (number) Page number for pagination
    - `limit`: (number) Results per page (max 200)

- `get_jobcode`: Get a specific jobcode by ID
  - Required Parameters:
    - `id`: (number) The ID of the jobcode to retrieve

- `get_jobcode_hierarchy`: Get complete jobcode hierarchy structure
  - Optional Parameters:
    - `name`: (string) Filter by name (use * as wildcard)
    - `type`: (string) Filter by type: "regular", "pto", "paid_break", "unpaid_break", "all"
    - `active`: (string) Filter by status: "yes", "no", "both"
    - `customfields`: (boolean) Include custom field data
    - `supplemental_data`: (string) Include supplemental data: "yes", "no"

### Timesheet Tools
- `get_timesheets`: Get timesheets with filtering
  - Parameters:
    - `modified_before`: (string) Filter by modification date
    - `modified_since`: (string) Filter by modification date
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_timesheet`: Get a specific timesheet by ID
  - Required Parameters:
    - `id`: (number) The ID of the timesheet to retrieve

- `get_current_timesheets`: Get currently active timesheets

### User Tools
- `get_users`: Get all users with filtering
  - Parameters:
    - `modified_before`: (string) Filter by modification date
    - `modified_since`: (string) Filter by modification date
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_user`: Get a specific user by ID
  - Required Parameters:
    - `id`: (number) The ID of the user to retrieve

- `get_current_user`: Get currently authenticated user

- `get_groups`: Get all groups from QuickBooks Time
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

### Project Management Tools
- `get_projects`: Get projects with filtering
  - Parameters:
    - `modified_before`: (string) Filter by modification date
    - `modified_since`: (string) Filter by modification date
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_project_activities`: Get project activities
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

### Reports Tools
- `get_current_totals`: Get current totals snapshot including shift and day totals
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_payroll`: Get payroll report
  - Required Parameters:
    - `start_date`: (string) Start date in YYYY-MM-DD format
    - `end_date`: (string) End date in YYYY-MM-DD format
  - Optional Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_payroll_by_jobcode`: Get payroll report grouped by jobcode
  - Required Parameters:
    - `start_date`: (string) Start date in YYYY-MM-DD format
    - `end_date`: (string) End date in YYYY-MM-DD format
  - Optional Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_project_report`: Get detailed project report with time entries
  - Required Parameters:
    - `start_date`: (string) Start date in YYYY-MM-DD format
    - `end_date`: (string) End date in YYYY-MM-DD format
    - `jobcode_ids`: (array of numbers) Filter by specific jobcode IDs
  - Optional Parameters:
    - `user_ids`: (array of numbers) Filter by specific user IDs
    - `group_ids`: (array of numbers) Filter by specific group IDs
    - `jobcode_type`: (string) Filter by type: "regular", "pto", "unpaid_break", "paid_break", "all"
    - `customfielditems`: (object) Filter by custom field items

### Additional Tools
- `get_custom_fields`: Get custom tracking fields configured on timecards
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_last_modified`: Get last modified timestamps for objects
  - Parameters:
    - `types`: (array of strings) Types of objects to check

- `get_notifications`: Get notifications
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

- `get_managed_clients`: Get managed clients
  - Parameters:
    - `page`: (number) Page number
    - `limit`: (number) Results per page

## Running the Server

```bash
python main.py
```

The server will start and listen for JSON-RPC requests on stdin/stdout.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Given that this project was developed with AI assistance, community input is especially valuable for improving and maintaining the codebase.

## Support

For issues and feature requests, please use the GitHub issues page or contact me directly at github.com/aallsbury.
