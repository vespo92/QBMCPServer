# QuickBooks Time MCP Server - Accountant's Guide

## What This Tool Does

This tool connects to your QuickBooks Time account and helps you:
- Generate payroll reports
- Track employee hours and overtime
- Monitor project costs and budgets
- Prepare client invoices
- Analyze time-off (PTO) usage
- Export data for tax preparation

## Common Accounting Tasks

### 1. Running Payroll

**What you might say:** "Show me payroll for last week"
**What the tool needs:** Start and end dates for the pay period

Example conversation:
```
You: "I need to run payroll for December 16-31, 2024"
Assistant: "I'll generate the payroll report for that period..."
```

The report will show:
- Total regular hours per employee
- Overtime hours (time and a half)
- Double-time hours
- PTO hours used
- Daily breakdown of hours

### 2. Client Billing

**What you might say:** "How many hours did we bill to ABC Company last month?"
**What the tool needs:** The project or job code name and date range

Example conversation:
```
You: "Show me all time billed to the ABC Company project in December"
Assistant: "I'll pull up all hours logged to ABC Company for December..."
```

### 3. Employee Time Tracking

**What you might say:** "Who's working right now?" or "Show me John's hours this week"
**What the tool needs:** Employee name or current status request

Example conversation:
```
You: "Is anyone still on the clock?"
Assistant: "Let me check who's currently working..."
```

### 4. PTO and Time Off Analysis

**What you might say:** "How much vacation time has Sarah used this year?"
**What the tool needs:** Employee name and time period

Example conversation:
```
You: "Check Sarah's PTO usage for 2024"
Assistant: "I'll look up Sarah's paid time off records for this year..."
```

## Understanding the Reports

### Payroll Report Fields
- **Regular Time (RE)**: Standard hourly work
- **Overtime (OT)**: Hours over 40 per week (usually 1.5x pay)
- **Double Time (DT)**: Holiday or special overtime (2x pay)
- **PTO**: Paid time off (vacation, sick leave)

### Time Formats
- All times are shown in seconds in the raw data
- To convert: seconds ÷ 3600 = hours
- Example: 28,800 seconds = 8 hours

### Common Terms Translation
- **Jobcode** = Project, Client, or Task
- **Timesheet** = Time entry or punch card
- **User** = Employee
- **Group** = Department or Team

## Frequently Asked Questions

### Q: How do I get last month's payroll?
A: Just ask for "payroll for last month" or specify the exact dates like "payroll from December 1 to December 31, 2024"

### Q: Can I see overtime trends?
A: Yes! Ask something like "Show me overtime hours by employee for the last 3 months"

### Q: How do I prepare client invoices?
A: Ask for "hours by project" or "time spent on [client name] project last month"

### Q: Can I track employee attendance?
A: Yes, you can ask "Show me who was late this week" or "List employees who worked on [specific date]"

### Q: How do I export data for taxes?
A: Request "annual payroll summary" or "Q4 payroll totals" - the data can be copied to Excel

## Tips for Best Results

1. **Be specific with dates**: Instead of "last week", say "December 16-22, 2024"
2. **Use employee names**: The system knows your employees by name
3. **Mention the purpose**: Say "for invoicing" or "for payroll" to get the right format
4. **Ask for summaries**: "Summarize overtime by department" works great

## Error Messages Explained

- **"No data found"**: Usually means no time was logged for that period
- **"Invalid date"**: Use format like "December 31, 2024" or "12/31/2024"
- **"User not found"**: Check the employee name spelling
- **"Access denied"**: You may need additional permissions in QuickBooks Time

## Getting Help

If you need to:
- Find a specific employee: Ask "List all employees"
- See all projects: Ask "Show me all active projects"
- Check job codes: Ask "What job codes do we use?"
- Understand a field: Ask "What does [field name] mean?"

Remember: You can always ask the assistant to explain any report or help you find the right information!