# QuickBooks Time MCP Server

A Message Control Protocol (MCP) server that provides unified access to QuickBooks Time API functionality. This server consolidates multiple QuickBooks Time services into a single, efficient interface.

## Important Note

I would LOVE help improving this project! Just glad to be able to give something back finally!

This entire project was developed and published using artificial intelligence (Claude), as I personally cannot write code. While every effort has been made to ensure quality and functionality, there may be imperfections or areas for improvement. I welcome any feedback, corrections, or suggestions from the community.

If you find any issues or have suggestions for improvements, please don't hesitate to open an issue or submit a pull request. Your expertise and input are greatly appreciated, as they will help make this project better for everyone.

## Features

- **Unified Interface**: Combines functionality from multiple QuickBooks Time services
- **JSON-RPC Based**: Simple, standardized communication protocol
- **Comprehensive API Coverage**: Full access to QuickBooks Time features
- **Efficient Processing**: Optimized for performance and reliability

## Prerequisites

- Python 3.8 or higher
- QuickBooks Time API access token
- Claude Desktop application
- Basic understanding of JSON-RPC

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aallsbury/qb-time-mcp-server.git
cd qb-time-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your QuickBooks Time access token

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

Save this as `config.json` in your Claude Desktop configuration directory. Make sure to:
1. Replace `your_quickbooks_time_access_token_here` with your actual QuickBooks Time access token
2. Adjust the path in `args` to point to where you cloned the repository
3. Update the `command` to point to your Python installation if needed

## Available Services

### JobCode Management
- Get all jobcodes with filtering options
- Retrieve specific jobcodes by ID
- Search jobcodes by name and criteria

### Reporting
- Access custom tracking fields
- Retrieve last modified timestamps
- Get current totals snapshots

### Timesheet Operations
- Retrieve timesheets with filtering
- Access specific timesheets by ID

### User Management
- Get all users with filtering options
- Retrieve specific users by ID
- Access currently authenticated user

## Usage

When properly configured in Claude Desktop, the server will automatically start when needed. You can interact with it through Claude using JSON-RPC requests.

Example request:
```json
{
    "jsonrpc": "2.0",
    "method": "get_jobcodes",
    "params": {"active": "yes"},
    "id": 1
}
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Given that this project was developed with AI assistance, community input is especially valuable for improving and maintaining the codebase.

## Support

For issues and feature requests, please use the GitHub issues page or contact me directly at github.com/aallsbury.
