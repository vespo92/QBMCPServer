# QuickBooks Time MCP Server for Accountants

A user-friendly MCP server that makes QuickBooks Time data accessible through natural language, designed specifically for accountants and bookkeepers.

## What This Does

This tool helps accountants:
- **Run Payroll** - Generate payroll reports with overtime and PTO tracking
- **Create Client Invoices** - Pull billable hours by project or client
- **Track Employee Time** - Monitor who's working, attendance, and hours
- **Analyze Costs** - Break down labor costs by project, department, or employee
- **Prepare Taxes** - Generate quarterly and annual tax reports
- **Manage PTO** - Track vacation and sick time usage and balances

## Key Features

✅ **Natural Language Support** - Say "payroll for last month" instead of using technical date formats  
✅ **Accounting Terms** - Uses familiar terms like "vacation" instead of "PTO", "employee" instead of "user"  
✅ **Friendly Error Messages** - Clear explanations when something goes wrong  
✅ **Pre-Built Workflows** - Common tasks like bi-weekly payroll are automated  
✅ **Smart Suggestions** - Recommends next steps after each action

## For Accountants

📚 **[Read the Accountant's Guide](ACCOUNTANT_GUIDE.md)** - Plain English guide with examples

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Setup

Create a `.env` file with your QuickBooks Time access token:
```
QB_TIME_ACCESS_TOKEN=your_access_token_here
NODE_ENV=production
```

### 3. Run the Server

For the enhanced accounting-friendly version:
```bash
python accounting_server.py
```

For the standard version:
```bash
python main.py
```

## Common Accounting Tasks

### Running Payroll
```
"Show me payroll for December 16-31, 2024"
"Get bi-weekly payroll ending yesterday"
"Show overtime hours for last month"
```

### Client Billing
```
"Hours for ABC Company project last month"
"Billable time by employee for Project X"
"Generate invoice data for Client Y"
```

### Employee Tracking
```
"Who's currently working?"
"Show John Smith's hours this week"
"List employees who haven't submitted timesheets"
```

### PTO Management
```
"Sarah's vacation usage this year"
"Remaining PTO balances for all employees"
"Who's scheduled off next week?"
```

## Claude Desktop Configuration

Add this to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "qb-time-accounting": {
      "command": "python",
      "args": ["path/to/accounting_server.py"],
      "env": {
        "QB_TIME_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Understanding Reports

### Time Conversions
- Raw data shows seconds
- 28,800 seconds = 8 hours
- 3,600 seconds = 1 hour

### Common Terms
- **Jobcode** = Project, Client, or Task
- **User** = Employee
- **Group** = Department or Team
- **RE** = Regular time
- **OT** = Overtime (1.5x)
- **DT** = Double time (2x)

## Available Tools

The server provides both standard API tools and accounting-specific workflows:

### Accounting Workflows
- `prepare_biweekly_payroll` - Complete bi-weekly payroll package
- `month_end_closing` - Month-end checklist and reports
- `quarterly_tax_prep` - Quarterly tax filing data
- `prepare_client_invoice` - Client billing with supporting docs
- `analyze_project_profitability` - Project cost analysis

### Standard API Tools
All the original QuickBooks Time API tools are available - see [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md) for complete details.

## Error Help

Common issues and solutions:

- **"No data found"** - No time entries exist for that period
- **"Invalid date"** - Use "December 31, 2024" or "12/31/2024"
- **"User not found"** - Check employee name spelling
- **"Access denied"** - Contact your QuickBooks Time admin

## Contributing

This project was developed with AI assistance to help bridge the gap between accounting needs and technical APIs. Your feedback is invaluable!

- Report issues: [GitHub Issues](https://github.com/yourusername/QBMCPServer/issues)
- Suggest features: Especially accounting workflows you'd find helpful
- Contribute code: PRs welcome, especially for accounting use cases

## License

MIT License - See LICENSE file for details

## Support

For help with:
- **QuickBooks Time API**: [QuickBooks Time Support](https://quickbooks.intuit.com/time-tracking/)
- **This Tool**: Create an issue on GitHub
- **Accounting Questions**: This tool provides data; consult your accounting professional for advice

---

Made with ❤️ for accountants by @aallsbury with AI assistance