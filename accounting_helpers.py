"""
Accounting-specific helper functions and natural language mappings
for QuickBooks Time MCP Server
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import re

class AccountingHelpers:
    """Helper functions to make the API more accountant-friendly"""
    
    # Natural language mappings for common accounting terms
    TERM_MAPPINGS = {
        # Time-related terms
        'last week': lambda: (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d'),
        'this week': lambda: datetime.now().strftime('%Y-%m-%d'),
        'last month': lambda: (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d'),
        'this month': lambda: datetime.now().replace(day=1).strftime('%Y-%m-%d'),
        'last quarter': lambda: AccountingHelpers._get_last_quarter_dates(),
        'this quarter': lambda: AccountingHelpers._get_current_quarter_dates(),
        'year to date': lambda: (datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')),
        'last year': lambda: (datetime.now().replace(year=datetime.now().year-1, month=1, day=1).strftime('%Y-%m-%d'),
                            datetime.now().replace(year=datetime.now().year-1, month=12, day=31).strftime('%Y-%m-%d')),
        
        # Accounting terms to API terms
        'vacation': 'pto',
        'sick leave': 'pto',
        'paid time off': 'pto',
        'holiday': 'pto',
        'regular hours': 'regular',
        'standard time': 'regular',
        'break': 'paid_break',
        'lunch': 'unpaid_break',
        'employee': 'user',
        'staff': 'user',
        'worker': 'user',
        'department': 'group',
        'team': 'group',
        'project': 'jobcode',
        'client': 'jobcode',
        'task': 'jobcode',
        'job': 'jobcode',
        'time entry': 'timesheet',
        'punch': 'timesheet',
        'clock in': 'timesheet',
        'hours worked': 'timesheet',
    }
    
    # Common date formats accountants use
    DATE_FORMATS = [
        '%m/%d/%Y',      # 12/31/2024
        '%m-%d-%Y',      # 12-31-2024
        '%B %d, %Y',     # December 31, 2024
        '%b %d, %Y',     # Dec 31, 2024
        '%d %B %Y',      # 31 December 2024
        '%Y-%m-%d',      # 2024-12-31 (ISO format)
    ]
    
    @staticmethod
    def parse_natural_date(date_str: str) -> str:
        """Convert natural language dates to YYYY-MM-DD format"""
        date_str = date_str.lower().strip()
        
        # Check for relative dates
        for term, func in AccountingHelpers.TERM_MAPPINGS.items():
            if term in date_str and callable(func):
                result = func()
                if isinstance(result, tuple):
                    return result[0]  # Return start date for ranges
                return result
        
        # Try parsing various date formats
        for fmt in AccountingHelpers.DATE_FORMATS:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If nothing matches, return original (API will validate)
        return date_str
    
    @staticmethod
    def _get_current_quarter_dates() -> Tuple[str, str]:
        """Get start and end dates for current quarter"""
        now = datetime.now()
        quarter = (now.month - 1) // 3
        start_month = quarter * 3 + 1
        start_date = now.replace(month=start_month, day=1)
        
        if start_month + 2 <= 12:
            end_date = now.replace(month=start_month + 2, day=1) + timedelta(days=31)
            end_date = end_date.replace(day=1) - timedelta(days=1)
        else:
            end_date = now.replace(month=12, day=31)
        
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    
    @staticmethod
    def _get_last_quarter_dates() -> Tuple[str, str]:
        """Get start and end dates for last quarter"""
        now = datetime.now()
        current_quarter = (now.month - 1) // 3
        
        if current_quarter == 0:
            # Last quarter of previous year
            start_date = now.replace(year=now.year-1, month=10, day=1)
            end_date = now.replace(year=now.year-1, month=12, day=31)
        else:
            start_month = (current_quarter - 1) * 3 + 1
            start_date = now.replace(month=start_month, day=1)
            end_date = now.replace(month=start_month + 2, day=1) + timedelta(days=31)
            end_date = end_date.replace(day=1) - timedelta(days=1)
        
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    
    @staticmethod
    def format_seconds_to_hours(seconds: int) -> str:
        """Convert seconds to human-readable hours format"""
        if not seconds:
            return "0 hours"
        
        hours = seconds / 3600
        if hours == int(hours):
            return f"{int(hours)} hours"
        else:
            return f"{hours:.2f} hours"
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format number as currency"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def translate_accounting_terms(text: str) -> str:
        """Translate common accounting terms to API terms"""
        text_lower = text.lower()
        for accounting_term, api_term in AccountingHelpers.TERM_MAPPINGS.items():
            if not callable(api_term) and accounting_term in text_lower:
                text = text.replace(accounting_term, api_term)
        return text
    
    @staticmethod
    def generate_friendly_error(error_msg: str) -> str:
        """Convert technical errors to accountant-friendly messages"""
        error_mappings = {
            'ISO 8601': 'Please use date format: MM/DD/YYYY or "December 31, 2024"',
            '404': 'The requested information was not found. Please check the employee name or date range.',
            '403': 'You don\'t have permission to access this information. Please contact your QuickBooks Time administrator.',
            '401': 'Your QuickBooks Time connection has expired. Please reconnect your account.',
            '429': 'Too many requests. Please wait a moment and try again.',
            'Invalid date': 'Please enter the date in format: MM/DD/YYYY',
            'No data': 'No time entries found for this period. Check if employees have logged their hours.',
            'required': 'This information is required to generate the report.',
        }
        
        for technical_term, friendly_message in error_mappings.items():
            if technical_term.lower() in error_msg.lower():
                return friendly_message
        
        return f"An error occurred: {error_msg}. Please try rephrasing your request or contact support."
    
    @staticmethod
    def suggest_next_action(completed_action: str) -> List[str]:
        """Suggest logical next steps after completing an action"""
        suggestions = {
            'payroll': [
                "Would you like to see overtime details?",
                "Should I generate a summary by department?",
                "Do you need to export this for your payroll system?",
                "Would you like to compare this to last pay period?"
            ],
            'invoice': [
                "Do you need to see the hourly breakdown by employee?",
                "Should I calculate the total billable amount?",
                "Would you like to mark these hours as invoiced?",
                "Do you need this broken down by task?"
            ],
            'timesheet': [
                "Would you like to approve these timesheets?",
                "Should I check for missing time entries?",
                "Do you need to see who hasn't submitted their timesheet?",
                "Would you like to see a weekly summary?"
            ],
            'pto': [
                "Would you like to see remaining PTO balances?",
                "Should I check who's scheduled for time off next week?",
                "Do you need a year-to-date PTO summary?",
                "Would you like to see PTO trends by department?"
            ]
        }
        
        for key, prompts in suggestions.items():
            if key in completed_action.lower():
                return prompts
        
        return ["Is there anything else you'd like to know about this data?"]
    
    @staticmethod
    def create_summary_header(report_type: str, start_date: str, end_date: str) -> str:
        """Create a friendly header for reports"""
        headers = {
            'payroll': f"📊 Payroll Report: {start_date} to {end_date}",
            'invoice': f"💰 Client Billing Report: {start_date} to {end_date}",
            'timesheet': f"⏰ Time Entry Report: {start_date} to {end_date}",
            'pto': f"🏖️ Time Off Report: {start_date} to {end_date}",
            'overtime': f"⏱️ Overtime Analysis: {start_date} to {end_date}",
        }
        
        return headers.get(report_type, f"📈 Report: {start_date} to {end_date}")
    
    @staticmethod
    def format_employee_summary(user_data: Dict[str, Any], timesheet_data: Optional[Dict[str, Any]] = None) -> str:
        """Format employee information in accountant-friendly way"""
        summary = []
        
        # Basic info
        summary.append(f"Employee: {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
        if user_data.get('employee_number'):
            summary.append(f"Employee #: {user_data.get('employee_number')}")
        
        # Time data if available
        if timesheet_data:
            if 'total_re_seconds' in timesheet_data:
                regular_hours = AccountingHelpers.format_seconds_to_hours(timesheet_data['total_re_seconds'])
                summary.append(f"Regular Hours: {regular_hours}")
            
            if 'total_ot_seconds' in timesheet_data and timesheet_data['total_ot_seconds'] > 0:
                ot_hours = AccountingHelpers.format_seconds_to_hours(timesheet_data['total_ot_seconds'])
                summary.append(f"Overtime Hours: {ot_hours}")
            
            if 'total_pto_seconds' in timesheet_data and timesheet_data['total_pto_seconds'] > 0:
                pto_hours = AccountingHelpers.format_seconds_to_hours(timesheet_data['total_pto_seconds'])
                summary.append(f"PTO Used: {pto_hours}")
        
        return "\n".join(summary)


class PayrollWorkflows:
    """Pre-built workflows for common payroll tasks"""
    
    @staticmethod
    def prepare_biweekly_payroll(api, end_date: str = None) -> Dict[str, Any]:
        """Prepare standard bi-weekly payroll with all necessary reports"""
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=13)
        start_date = start_dt.strftime('%Y-%m-%d')
        
        return {
            'period': f"{start_date} to {end_date}",
            'reports_needed': [
                'payroll_summary',
                'overtime_report',
                'pto_usage',
                'department_breakdown'
            ],
            'next_steps': [
                'Review overtime for compliance',
                'Verify PTO balances',
                'Export to payroll system',
                'Generate pay stubs'
            ]
        }
    
    @staticmethod
    def month_end_closing(api, month: int = None, year: int = None) -> Dict[str, Any]:
        """Month-end closing checklist and reports"""
        if not month:
            month = datetime.now().month - 1 if datetime.now().month > 1 else 12
        if not year:
            year = datetime.now().year if month != 12 else datetime.now().year - 1
        
        return {
            'month': f"{month}/{year}",
            'checklist': [
                '✓ All timesheets submitted',
                '✓ Overtime approved',
                '✓ PTO balances updated',
                '✓ Client hours verified',
                '✓ Project budgets reviewed'
            ],
            'reports': [
                'monthly_payroll_summary',
                'client_billing_summary',
                'project_profitability',
                'employee_utilization'
            ]
        }
    
    @staticmethod
    def quarterly_tax_prep(api, quarter: int = None, year: int = None) -> Dict[str, Any]:
        """Prepare quarterly tax filing data"""
        if not quarter:
            quarter = (datetime.now().month - 1) // 3
        if not year:
            year = datetime.now().year
        
        return {
            'quarter': f"Q{quarter} {year}",
            'required_data': [
                'Total wages by employee',
                'Total hours worked',
                'Overtime wages',
                'PTO payouts',
                'State-by-state breakdown'
            ],
            'forms': [
                'Form 941 data',
                'State quarterly returns',
                'Workers comp report'
            ]
        }


class InvoiceWorkflows:
    """Pre-built workflows for client invoicing"""
    
    @staticmethod
    def prepare_client_invoice(api, client_name: str, start_date: str, end_date: str, 
                             hourly_rate: float = None) -> Dict[str, Any]:
        """Prepare a client invoice with all supporting documentation"""
        return {
            'client': client_name,
            'period': f"{start_date} to {end_date}",
            'components': [
                'Hours by employee',
                'Hours by task/project',
                'Daily breakdown',
                'Expense summary'
            ],
            'calculations': {
                'hourly_rate': hourly_rate or 'Use standard rates',
                'total_hours': 'To be calculated',
                'total_amount': 'To be calculated'
            },
            'attachments': [
                'Detailed time log',
                'Project milestone report',
                'Expense receipts'
            ]
        }
    
    @staticmethod
    def analyze_project_profitability(api, project_name: str, 
                                    start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Analyze project profitability with cost breakdown"""
        return {
            'project': project_name,
            'analysis': [
                'Total hours by employee',
                'Labor costs',
                'Budgeted vs actual hours',
                'Billing vs cost rates',
                'Profit margin'
            ],
            'recommendations': [
                'Staffing adjustments',
                'Rate negotiations',
                'Scope management'
            ]
        }