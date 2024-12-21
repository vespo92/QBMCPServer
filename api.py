import requests
from typing import Dict, Any, Optional, List, Union
from utils import setup_logging, log_info, log_error
from datetime import datetime

class BaseAPI:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = 'https://rest.tsheets.com/api/v1'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def format_date_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Format date parameters.
        - modified_since and modified_before are converted to ISO-8601 format
        - start_date and end_date stay in YYYY-MM-DD format
        """
        iso_fields = ['modified_since', 'modified_before']
        formatted_params = params.copy()
        
        # Convert ISO fields to ISO-8601 format
        for field in iso_fields:
            if field in formatted_params and formatted_params[field]:
                # If it's already in ISO format, leave it
                if 'T' in str(formatted_params[field]):
                    continue
                    
                try:
                    # Parse the date and convert to ISO format
                    date = datetime.strptime(str(formatted_params[field]), '%Y-%m-%d')
                    formatted_params[field] = date.strftime('%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    # If it's not in expected format, leave it unchanged
                    continue
                    
        return formatted_params

    def add_pagination_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Clean up undefined and null values
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        # Format date parameters
        clean_params = self.format_date_params(clean_params)

        # Convert arrays to comma-separated strings if present, except jobcode_ids
        for key, value in clean_params.items():
            if isinstance(value, list):
                if key == 'jobcode_ids':
                    # Convert jobcode_ids to array of strings but keep as array
                    clean_params[key] = [str(x) for x in value]
                else:
                    clean_params[key] = ','.join(map(str, value))

        # Ensure limit doesn't exceed 200
        if 'limit' in clean_params:
            clean_params['limit'] = min(clean_params['limit'], 200)

        return clean_params

    def handle_axios_error(self, error: Exception, operation: str):
        if isinstance(error, requests.exceptions.RequestException):
            if error.response is not None:
                # The request was made and the server responded with a status code
                # that falls out of the range of 2xx
                error_message = error.response.json().get('error', {}).get('message') or error.response.reason
                log_error(f"{operation} failed: {error.response.status_code} - {error_message}")
                raise ValueError(f"{operation} failed: {error.response.status_code} - {error_message}")
            elif error.request is not None:
                # The request was made but no response was received
                log_error(f"{operation} failed: No response received")
                raise ValueError(f"{operation} failed: No response received from server")
            else:
                # Something happened in setting up the request
                log_error(f"{operation} failed: {str(error)}")
                raise ValueError(f"{operation} failed: {str(error)}")
        else:
            log_error(f"{operation} failed: {str(error)}")
            raise ValueError(f"{operation} failed: {str(error)}")

    def make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """Make a request to the QuickBooks Time API."""
        try:
            response = requests.get(f'{self.base_url}/{endpoint}', headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as error:
            return self.handle_axios_error(error, f'API request to {endpoint}')

class JobcodeAPI(BaseAPI):
    def get_jobcodes(self, params: Optional[Dict[str, Any]] = None):
        """Get jobcodes with optional filters."""
        params = self.add_pagination_params(params)
        return self.make_request('jobcodes', params=params)

    def get_jobcode(self, id: Union[int, Dict[str, int]]) -> Dict[str, Any]:
        """Get a specific jobcode by ID."""
        # Extract the numeric ID, handling both number and object formats
        jobcode_id = id['id'] if isinstance(id, dict) else id
        
        try:
            # Validate ID format
            if not isinstance(jobcode_id, int) or jobcode_id <= 0:
                raise ValueError('Invalid jobcode ID format')

            response = requests.get(
                f'{self.base_url}/jobcodes',
                headers=self.headers,
                params={
                    'ids': jobcode_id,
                    'active': 'both',
                    'supplemental_data': 'yes'
                }
            )
            response.raise_for_status()
            data = response.json()

            jobcodes = data.get('results', {}).get('jobcodes', {})
            if not jobcodes:
                raise ValueError('No jobcodes found in response')

            jobcode = jobcodes.get(str(jobcode_id))
            if not jobcode:
                raise ValueError(f'Jobcode {jobcode_id} not found. It may be deleted or you may not have access.')

            return {'result': jobcode}

        except requests.exceptions.RequestException as error:
            if error.response is not None:
                if error.response.status_code == 403:
                    raise ValueError(f'Permission denied for jobcode {jobcode_id}. Please verify your access rights.')
                elif error.response.status_code == 429:
                    raise ValueError('Rate limit exceeded. Please try again later.')
                elif error.response.status_code == 417:
                    raise ValueError('Invalid jobcode ID format. Must be a positive integer.')

            return self.handle_axios_error(error, f'Fetching jobcode {jobcode_id}')

    def get_jobcode_hierarchy(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get the jobcode hierarchy structure."""
        try:
            # Start with top-level jobcodes (parent_id = 0)
            response = requests.get(
                f'{self.base_url}/jobcodes',
                headers=self.headers,
                params=self.add_pagination_params({
                    **(params or {}),
                    'parent_ids': 0,  # Get only top-level jobcodes
                    'supplemental_data': 'yes',
                    'limit': 200
                })
            )
            response.raise_for_status()
            data = response.json()

            jobcodes = data.get('results', {}).get('jobcodes', {})
            if not jobcodes:
                return {'results': []}

            root_jobcodes = list(jobcodes.values())
            jobcodes_with_children = []

            # For each jobcode that has children, fetch its children
            for jobcode in root_jobcodes:
                if jobcode.get('has_children'):
                    try:
                        child_response = requests.get(
                            f'{self.base_url}/jobcodes',
                            headers=self.headers,
                            params=self.add_pagination_params({
                                'parent_ids': jobcode['id'],
                                'supplemental_data': 'yes',
                                'limit': 200
                            })
                        )
                        child_response.raise_for_status()
                        child_data = child_response.json()
                        children = list(child_data.get('results', {}).get('jobcodes', {}).values())
                        jobcode['children'] = children
                        jobcodes_with_children.append(jobcode)
                    except Exception as error:
                        log_error(f"Error fetching children for jobcode {jobcode['id']}: {str(error)}")
                        jobcode['children'] = []
                        jobcodes_with_children.append(jobcode)
                else:
                    jobcode['children'] = []
                    jobcodes_with_children.append(jobcode)

            return {'results': jobcodes_with_children}
        except Exception as error:
            return self.handle_axios_error(error, 'Fetching jobcode hierarchy')

    def get_timesheets(self, params: Optional[Dict[str, Any]] = None):
        """Get timesheets with optional filters."""
        params = self.add_pagination_params(params)
        return self.make_request('timesheets', params=params)

    def get_timesheet(self, id: Union[int, Dict[str, int]]):
        """Get a specific timesheet by ID."""
        if isinstance(id, dict):
            id = id.get('id')
        return self.make_request(f'timesheets/{id}')

    def get_current_timesheets(self):
        """Get currently active timesheets."""
        return self.make_request('timesheets/current')

class TimesheetAPI(BaseAPI):
    def get_timesheets(self, params: Optional[Dict[str, Any]] = None):
        """Get timesheets with optional filters."""
        params = self.add_pagination_params(params)
        return self.make_request('timesheets', params=params)

    def get_timesheet(self, id: Union[int, Dict[str, int]]):
        """Get a specific timesheet by ID."""
        if isinstance(id, dict):
            id = id.get('id')
        return self.make_request(f'timesheets/{id}')

    def get_current_timesheets(self):
        """Get currently active timesheets."""
        return self.make_request('timesheets/current')

class UserAPI(BaseAPI):
    def get_users(self, params: Optional[Dict[str, Any]] = None):
        """Get users with optional filters."""
        params = self.add_pagination_params(params)
        return self.make_request('users', params=params)

    def get_user(self, id: Union[int, Dict[str, int]]):
        """Get a specific user by ID."""
        if isinstance(id, dict):
            id = id.get('id')
        return self.make_request(f'users/{id}')

    def get_current_user(self):
        """Get details about the currently authenticated user."""
        return self.make_request('current_user')

    def get_groups(self, params: Optional[Dict[str, Any]] = None):
        """Get all groups from QuickBooks Time."""
        params = self.add_pagination_params(params)
        return self.make_request('groups', params=params)

class CustomFieldsAPI(BaseAPI):
    def get_custom_fields(self, params: Optional[Dict[str, Any]] = None):
        """Get custom tracking fields configured on timecards."""
        params = self.add_pagination_params(params)
        return self.make_request('customfields', params=params)

class ProjectManagementAPI(BaseAPI):
    def get_projects(self, params: Optional[Dict[str, Any]] = None):
        """Get projects with optional filters."""
        params = self.add_pagination_params(params)
        return self.make_request('projects', params=params)

    def get_project_activities(self, params: Optional[Dict[str, Any]] = None):
        """Get project activities."""
        params = self.add_pagination_params(params)
        return self.make_request('project_activities', params=params)

class LastModifiedAPI(BaseAPI):
    def get_last_modified(self, types: list = None):
        """Get last modified timestamps for objects."""
        params = {'types': ','.join(types) if types else None}
        params = self.add_pagination_params(params)
        return self.make_request('last_modified_timestamps', params=params)

class NotificationsAPI(BaseAPI):
    def get_notifications(self, params: Optional[Dict[str, Any]] = None):
        """Get notifications."""
        params = self.add_pagination_params(params)
        return self.make_request('notifications', params=params)

class AdditionalFeaturesAPI(BaseAPI):
    def get_managed_clients(self, params: Optional[Dict[str, Any]] = None):
        """Get managed clients."""
        params = self.add_pagination_params(params)
        return self.make_request('managed_clients', params=params)

class ReportsAPI(BaseAPI):
    def get_current_totals(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            query_params = self.add_pagination_params(params)
            response = requests.get(
                f'{self.base_url}/reports/current_totals',
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            return self.handle_axios_error(error, 'Fetching current totals')

    def get_payroll(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query_params = self.add_pagination_params(params)
            response = requests.get(
                f'{self.base_url}/reports/payroll',
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            return self.handle_axios_error(error, 'Fetching payroll report')

    def get_payroll_by_jobcode(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query_params = self.add_pagination_params(params)
            response = requests.get(
                f'{self.base_url}/reports/payroll_by_jobcode',
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            return self.handle_axios_error(error, 'Fetching payroll by jobcode report')

    def get_project_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            data = {'data': self.add_pagination_params(params)}
            response = requests.post(
                f'{self.base_url}/reports/project',
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            return self.handle_axios_error(error, 'Fetching project report')

class QuickBooksTimeAPI(BaseAPI):
    def __init__(self, access_token: str):
        super().__init__(access_token)
        self.jobcode_api = JobcodeAPI(access_token)
        self.timesheet_api = TimesheetAPI(access_token)
        self.user_api = UserAPI(access_token)
        self.custom_fields_api = CustomFieldsAPI(access_token)
        self.project_management_api = ProjectManagementAPI(access_token)
        self.last_modified_api = LastModifiedAPI(access_token)
        self.notifications_api = NotificationsAPI(access_token)
        self.additional_features_api = AdditionalFeaturesAPI(access_token)
        self.reports_api = ReportsAPI(access_token)
        self.validate_token()

    def validate_token(self) -> bool:
        try:
            response = requests.get(
                f'{self.base_url}/current_user',
                headers=self.headers
            )
            response.raise_for_status()
            log_info('Token validation successful')
            return True
        except requests.exceptions.RequestException as error:
            if error.response is not None:
                raise ValueError(f'Token validation failed: {error.response.status_code} - {error.response.reason}')
            elif error.request is not None:
                raise ValueError('Token validation failed: No response received from server')
            else:
                raise ValueError(f'Token validation failed: {str(error)}')

    def get_jobcodes(self, params: Optional[Dict[str, Any]] = None):
        return self.jobcode_api.get_jobcodes(params)

    def get_jobcode(self, params: Dict[str, Any]):
        return self.jobcode_api.get_jobcode(params.get('id'))

    def search_jobcodes(self, params: Dict[str, Any]):
        return self.jobcode_api.search_jobcodes(params)

    def get_jobcode_hierarchy(self, params: Optional[Dict[str, Any]] = None):
        return self.jobcode_api.get_jobcode_hierarchy(params)

    def get_timesheets(self, params: Optional[Dict[str, Any]] = None):
        return self.timesheet_api.get_timesheets(params)

    def get_timesheet(self, params: Dict[str, Any]):
        return self.timesheet_api.get_timesheet(params.get('id'))

    def get_current_timesheets(self, params: Optional[Dict[str, Any]] = None):
        return self.timesheet_api.get_current_timesheets()

    def get_users(self, params: Optional[Dict[str, Any]] = None):
        return self.user_api.get_users(params)

    def get_user(self, params: Dict[str, Any]):
        return self.user_api.get_user(params.get('id'))

    def get_current_user(self, params: Optional[Dict[str, Any]] = None):
        return self.user_api.get_current_user()

    def get_groups(self, params: Optional[Dict[str, Any]] = None):
        return self.user_api.get_groups(params)

    def get_custom_fields(self, params: Optional[Dict[str, Any]] = None):
        return self.custom_fields_api.get_custom_fields(params)

    def get_projects(self, params: Optional[Dict[str, Any]] = None):
        return self.project_management_api.get_projects(params)

    def get_project_activities(self, params: Optional[Dict[str, Any]] = None):
        return self.project_management_api.get_project_activities(params)

    def get_last_modified(self, params: Optional[Dict[str, Any]] = None):
        return self.last_modified_api.get_last_modified(params.get('types'))

    def get_notifications(self, params: Optional[Dict[str, Any]] = None):
        return self.notifications_api.get_notifications(params)

    def get_managed_clients(self, params: Optional[Dict[str, Any]] = None):
        return self.additional_features_api.get_managed_clients(params)

    def get_current_totals(self, params: Optional[Dict[str, Any]] = None):
        return self.reports_api.get_current_totals(params)

    def get_payroll(self, params: Dict[str, Any]):
        return self.reports_api.get_payroll(params)

    def get_payroll_by_jobcode(self, params: Dict[str, Any]):
        return self.reports_api.get_payroll_by_jobcode(params)

    def get_project_report(self, params: Dict[str, Any]):
        return self.reports_api.get_project_report(params)
