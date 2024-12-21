# QuickBooks Time MCP Server (Combined)

This is a combined MCP server that provides access to all QuickBooks Time API functionality through a single interface. It combines the functionality of four separate servers:

1. JobCode Tools
2. Reports & Core Tools
3. Timesheet Tools
4. User Tools

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your QuickBooks Time access token:
```
QB_TIME_ACCESS_TOKEN=your_access_token_here
NODE_ENV=development
```

## Available Tools

### JobCode Tools
- `get_jobcodes`: Get all jobcodes with filtering options
- `get_jobcode`: Get a specific jobcode by ID
- `search_jobcodes`: Search jobcodes by name and criteria

### Reports & Core Tools
- `get_custom_fields`: Get custom tracking fields
- `get_last_modified`: Get last modified timestamps
- `get_current_totals`: Get current totals snapshot

### Timesheet Tools
- `get_timesheets`: Get timesheets with filtering
- `get_timesheet`: Get a specific timesheet by ID

### User Tools
- `get_users`: Get all users with filtering
- `get_user`: Get a specific user by ID
- `get_current_user`: Get currently authenticated user

## Running the Server

```bash
python main.py
```

The server will start and listen for JSON-RPC requests on stdin/stdout.
