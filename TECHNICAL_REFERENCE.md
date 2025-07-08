# Technical Reference - QuickBooks Time MCP Server

This document contains the complete technical reference for all available API tools.

## API Tools Reference

### JobCode Tools

#### get_jobcodes
Get jobcodes with advanced filtering options.

**Parameters:**
- `ids` (array of numbers, optional): Filter by specific jobcode IDs
- `name` (string, optional): Filter by name, supports wildcard (*) matching
- `active` (string, optional): Filter by status: "yes", "no", "both" (default: "yes")
- `type` (string, optional): Filter by type: "regular", "pto", "paid_break", "unpaid_break", "all"
- `parent_ids` (array of numbers, optional): Filter by parent IDs (0=top-level, -1=all)
- `customfields` (boolean, optional): Include custom fields
- `modified_before` (string, optional): ISO 8601 date
- `modified_since` (string, optional): ISO 8601 date
- `page` (number): Page number
- `limit` (number): Results per page (max 200)

#### get_jobcode
Get a specific jobcode by ID.

**Parameters:**
- `id` (number, required): The jobcode ID
- `customfields` (boolean, optional): Include custom fields

#### get_jobcode_hierarchy
Get complete jobcode hierarchy structure.

**Parameters:**
- `parent_ids` (array of numbers, optional): Filter by parent IDs
- `active` (string, optional): Filter by status
- `type` (string, optional): Filter by type

### Timesheet Tools

#### get_timesheets
Get timesheets with filtering. Requires at least one of: ids, start_date, modified_before, or modified_since.

**Parameters:**
- `ids` (array of numbers): Timesheet IDs
- `start_date` (string): YYYY-MM-DD format
- `end_date` (string): YYYY-MM-DD format
- `user_ids` (array of numbers): Filter by users
- `group_ids` (array of numbers): Filter by groups
- `jobcode_ids` (array of numbers): Filter by jobcodes
- `payroll_ids` (array of numbers): Filter by payroll IDs
- `on_the_clock` (string): "yes", "no", "both"
- `jobcode_type` (string): Filter by type
- `page` (number): Page number
- `limit` (number): Results per page

#### get_timesheet
Get a specific timesheet by ID.

**Parameters:**
- `id` (number, required): Timesheet ID

#### get_current_timesheets
Get currently active timesheets.

**Parameters:**
- `user_ids` (array of numbers, optional): Filter by users
- `group_ids` (array of numbers, optional): Filter by groups
- `jobcode_ids` (array of numbers, optional): Filter by jobcodes
- `supplemental_data` (string, optional): "yes" or "no"

### User Tools

#### get_users
Get all users with filtering.

**Parameters:**
- `ids` (array of numbers): Filter by user IDs
- `not_ids` (array of numbers): Exclude user IDs
- `employee_numbers` (array of numbers): Filter by employee numbers
- `usernames` (array of strings): Filter by usernames
- `group_ids` (array of numbers): Filter by groups
- `not_group_ids` (array of numbers): Exclude groups
- `payroll_ids` (array of strings): Filter by payroll IDs
- `active` (string): "yes", "no", "both"
- `first_name` (string): Filter by first name
- `last_name` (string): Filter by last name
- `modified_before` (string): ISO 8601 date
- `modified_since` (string): ISO 8601 date
- `page` (number): Page number
- `per_page` (number): Results per page

#### get_user
Get a specific user by ID.

**Parameters:**
- `id` (number, required): User ID

#### get_current_user
Get currently authenticated user. No parameters required.

#### get_groups
Get all groups.

**Parameters:**
- `ids` (array of numbers): Filter by group IDs
- `active` (string): "yes", "no", "both"
- `manager_ids` (array of numbers): Filter by managers
- `supplemental_data` (string): "yes", "no"

### Project Management Tools

#### get_projects
Get projects with filtering.

**Parameters:**
- `ids` (array of numbers): Project IDs
- `active` (string): "yes", "no", "both"
- `client_id` (number): Filter by client
- `jobcode_id` (number): Filter by jobcode
- `modified_before` (string): ISO 8601 date
- `modified_since` (string): ISO 8601 date
- `page` (number): Page number
- `per_page` (number): Results per page

#### get_project_activities
Get project activity logs.

**Parameters:**
- `project_ids` (array of numbers): Filter by projects
- `user_ids` (array of numbers): Filter by users
- `activity_types` (array of strings): Filter by type
- `modified_before` (string): ISO 8601 date
- `modified_since` (string): ISO 8601 date
- `page` (number): Page number
- `per_page` (number): Results per page

### Reports Tools

#### get_current_totals
Get current totals snapshot.

**Parameters:**
- `user_ids` (array of numbers): Filter by users
- `group_ids` (array of numbers): Filter by groups
- `jobcode_ids` (array of numbers): Filter by jobcodes
- `on_the_clock` (string): "yes", "no", "both"
- `page` (number): Page number
- `limit` (number): Results per page

#### get_payroll
Get payroll report.

**Required Parameters:**
- `start_date` (string): YYYY-MM-DD format
- `end_date` (string): YYYY-MM-DD format

**Optional Parameters:**
- `user_ids` (array of numbers): Filter by users
- `group_ids` (array of numbers): Filter by groups
- `include_zero_time` (boolean): Include users with no time

#### get_payroll_by_jobcode
Get payroll report grouped by jobcode.

**Required Parameters:**
- `start_date` (string): YYYY-MM-DD format
- `end_date` (string): YYYY-MM-DD format

**Optional Parameters:**
- `user_ids` (array of numbers): Filter by users
- `group_ids` (array of numbers): Filter by groups
- `jobcode_ids` (array of numbers): Filter by jobcodes
- `jobcode_type` (string): Filter by type
- `include_zero_time` (boolean): Include empty jobcodes

#### get_project_report
Get detailed project report.

**Required Parameters:**
- `start_date` (string): YYYY-MM-DD format
- `end_date` (string): YYYY-MM-DD format

**Optional Parameters:**
- `user_ids` (array of numbers): Filter by users
- `group_ids` (array of numbers): Filter by groups
- `jobcode_ids` (array of numbers): Filter by jobcodes
- `jobcode_type` (string): Filter by type
- `customfielditems` (object): Filter by custom fields

### Additional Tools

#### get_custom_fields
Get custom tracking fields.

**Parameters:**
- `ids` (array of numbers): Filter by field IDs
- `active` (string): "yes", "no", "both"
- `applies_to` (string): "timesheet", "jobcode", "user"
- `value_type` (string): "managed-list", "free-form"
- `page` (number): Page number
- `limit` (number): Results per page

#### get_last_modified
Get last modified timestamps.

**Parameters:**
- `types` (array of strings): Object types to check

#### get_notifications
Get notifications.

**Parameters:**
- `page` (number): Page number
- `limit` (number): Results per page

#### get_managed_clients
Get managed clients.

**Parameters:**
- `page` (number): Page number
- `limit` (number): Results per page

## Response Formats

### Timesheet Object
```json
{
  "id": 123456,
  "user_id": 789,
  "jobcode_id": 456,
  "start": "2024-01-15T08:00:00-05:00",
  "end": "2024-01-15T17:00:00-05:00",
  "date": "2024-01-15",
  "duration": 32400,
  "locked": 0,
  "notes": "Client meeting",
  "customfields": {},
  "last_modified": "2024-01-15T17:05:00-05:00"
}
```

### User Object
```json
{
  "id": 789,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@company.com",
  "employee_number": 12345,
  "active": true,
  "group_id": 123,
  "payroll_id": "EMP123",
  "hire_date": "2020-01-15",
  "last_active": "2024-01-15T17:00:00-05:00"
}
```

### Payroll Report Object
```json
{
  "totals": {
    "total_re_seconds": 288000,
    "total_ot_seconds": 10800,
    "total_dt_seconds": 0,
    "total_pto_seconds": 0,
    "total_work_seconds": 298800
  },
  "by_user": {
    "789": {
      "total_re_seconds": 144000,
      "total_ot_seconds": 5400,
      "timesheet_count": 5
    }
  }
}
```

## Error Codes

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Invalid or expired token
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource doesn't exist
- `429` - Too Many Requests: Rate limit exceeded
- `500` - Internal Server Error: API error

## Rate Limits

- 300 requests per minute per access token
- 3 requests per second sustained rate
- Implement exponential backoff on 429 errors

## Date/Time Formats

- Dates: YYYY-MM-DD (e.g., "2024-01-15")
- Timestamps: ISO 8601 (e.g., "2024-01-15T08:00:00-05:00")
- Durations: Seconds (e.g., 3600 = 1 hour)

## Pagination

- Default page size: 50
- Maximum page size: 200
- Use `page` parameter to navigate
- Check `more` field in response for additional pages