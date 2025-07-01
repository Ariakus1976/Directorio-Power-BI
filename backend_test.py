#!/usr/bin/env python3
import requests
import json
import sys
from typing import Dict, Any, List, Optional

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://48ef11f4-6b93-4753-a4b0-eb29da7e5375.preview.emergentagent.com"
API_BASE_URL = f"{BACKEND_URL}/api"

# Expected work areas
EXPECTED_WORK_AREAS = [
    "DIRECCION COMERCIAL", 
    "COMERCIALES", 
    "COMPRAS", 
    "RECURSOS HUMANOS", 
    "GERENCIA", 
    "SUCURSALES", 
    "ALTEC"
]

# Expected total number of reports
EXPECTED_TOTAL_REPORTS = 46

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test_header(test_name: str) -> None:
    """Print a formatted test header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}Running Test: {test_name}{Colors.ENDC}")

def print_test_result(success: bool, message: str) -> None:
    """Print a formatted test result"""
    if success:
        print(f"{Colors.OKGREEN}✓ PASS: {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ FAIL: {message}{Colors.ENDC}")

def make_request(endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Make a request to the API and return the response"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}Error making request to {url}: {str(e)}{Colors.ENDC}")
        return {"success": False, "error": str(e)}

def test_health_check() -> bool:
    """Test 1: Basic Health Check - Test the root endpoint"""
    print_test_header("Basic Health Check")
    
    try:
        # The root endpoint is at / not /api/
        response = requests.get(f"{BACKEND_URL}/")
        response.raise_for_status()
        data = response.json()
        
        success = "message" in data and "Power BI Directory API is running" in data["message"]
        print_test_result(success, "Health check endpoint is working")
        
        if not success:
            print(f"{Colors.WARNING}Unexpected response: {data}{Colors.ENDC}")
        
        return success
    except Exception as e:
        print_test_result(False, f"Health check failed: {str(e)}")
        return False

def test_reports_api() -> bool:
    """Test 2: Reports API - Test /api/reports endpoint"""
    print_test_header("Reports API")
    
    response = make_request("/reports")
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a list
    data_exists = "data" in response and isinstance(response["data"], list)
    print_test_result(data_exists, "Response has data field with a list of reports")
    
    # Check if total field exists and matches the length of data
    total_correct = "total" in response and response["total"] == len(response["data"])
    print_test_result(total_correct, "Total field matches the number of reports returned")
    
    # Check if we have the expected number of reports
    expected_count = "total" in response and response["total"] == EXPECTED_TOTAL_REPORTS
    print_test_result(expected_count, f"Found expected number of reports ({EXPECTED_TOTAL_REPORTS})")
    
    if not expected_count and "total" in response:
        print(f"{Colors.WARNING}Found {response['total']} reports, expected {EXPECTED_TOTAL_REPORTS}{Colors.ENDC}")
    
    # Check report structure (first report)
    if data_exists and len(response["data"]) > 0:
        first_report = response["data"][0]
        fields = ["id", "name", "group", "url", "created_at", "updated_at"]
        has_all_fields = all(field in first_report for field in fields)
        print_test_result(has_all_fields, "Reports have the expected fields")
        
        if not has_all_fields:
            missing = [field for field in fields if field not in first_report]
            print(f"{Colors.WARNING}Missing fields: {', '.join(missing)}{Colors.ENDC}")
    
    return success_field and data_exists and total_correct and expected_count

def test_groups_api() -> bool:
    """Test 3: Groups API - Test /api/groups endpoint"""
    print_test_header("Groups API")
    
    response = make_request("/groups")
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a list
    data_exists = "data" in response and isinstance(response["data"], list)
    print_test_result(data_exists, "Response has data field with a list of groups")
    
    # Check if we have the expected number of work areas
    if data_exists:
        groups = response["data"]
        expected_count = len(groups) == len(EXPECTED_WORK_AREAS)
        print_test_result(expected_count, f"Found expected number of work areas ({len(EXPECTED_WORK_AREAS)})")
        
        if not expected_count:
            print(f"{Colors.WARNING}Found {len(groups)} work areas, expected {len(EXPECTED_WORK_AREAS)}{Colors.ENDC}")
        
        # Check if all expected work areas are present
        all_areas_present = all(area in groups for area in EXPECTED_WORK_AREAS)
        print_test_result(all_areas_present, "All expected work areas are present")
        
        if not all_areas_present:
            missing = [area for area in EXPECTED_WORK_AREAS if area not in groups]
            print(f"{Colors.WARNING}Missing work areas: {', '.join(missing)}{Colors.ENDC}")
            
            unexpected = [area for area in groups if area not in EXPECTED_WORK_AREAS]
            if unexpected:
                print(f"{Colors.WARNING}Unexpected work areas: {', '.join(unexpected)}{Colors.ENDC}")
    
    return success_field and data_exists

def test_stats_api() -> bool:
    """Test 4: Stats API - Test /api/stats endpoint"""
    print_test_header("Stats API")
    
    response = make_request("/stats")
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists
    data_exists = "data" in response and isinstance(response["data"], dict)
    print_test_result(data_exists, "Response has data field with statistics")
    
    if data_exists:
        # Check if total_reports field exists
        total_reports_exists = "total_reports" in response["data"]
        print_test_result(total_reports_exists, "Response has total_reports field")
        
        # Check if total_reports matches expected count
        if total_reports_exists:
            total_correct = response["data"]["total_reports"] == EXPECTED_TOTAL_REPORTS
            print_test_result(total_correct, f"Total reports matches expected count ({EXPECTED_TOTAL_REPORTS})")
            
            if not total_correct:
                print(f"{Colors.WARNING}Found {response['data']['total_reports']} reports, expected {EXPECTED_TOTAL_REPORTS}{Colors.ENDC}")
        
        # Check if groups field exists and is a list
        groups_exist = "groups" in response["data"] and isinstance(response["data"]["groups"], list)
        print_test_result(groups_exist, "Response has groups field with statistics")
        
        # Check if group stats have the expected structure
        if groups_exist and len(response["data"]["groups"]) > 0:
            first_group = response["data"]["groups"][0]
            has_correct_structure = "_id" in first_group and "count" in first_group
            print_test_result(has_correct_structure, "Group statistics have the expected structure")
    
    return success_field and data_exists

def test_filtering_by_group() -> bool:
    """Test 5: Filtering - Test /api/reports?group=COMERCIALES"""
    print_test_header("Filtering by Group")
    
    group_to_test = "COMERCIALES"
    response = make_request("/reports", {"group": group_to_test})
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a list
    data_exists = "data" in response and isinstance(response["data"], list)
    print_test_result(data_exists, "Response has data field with a list of reports")
    
    # Check if all reports belong to the specified group
    if data_exists and len(response["data"]) > 0:
        all_in_group = all(report["group"] == group_to_test for report in response["data"])
        print_test_result(all_in_group, f"All reports belong to the {group_to_test} group")
        
        if not all_in_group:
            incorrect = [report["name"] for report in response["data"] if report["group"] != group_to_test]
            print(f"{Colors.WARNING}Reports with incorrect group: {', '.join(incorrect)}{Colors.ENDC}")
        
        # Check if we got at least one report
        has_reports = len(response["data"]) > 0
        print_test_result(has_reports, f"Found reports for the {group_to_test} group")
        
        if has_reports:
            print(f"{Colors.OKBLUE}Found {len(response['data'])} reports in the {group_to_test} group{Colors.ENDC}")
    
    return success_field and data_exists

def test_search_functionality() -> bool:
    """Test 6: Search - Test /api/reports?search=ventas"""
    print_test_header("Search Functionality")
    
    search_term = "ventas"
    response = make_request("/reports", {"search": search_term})
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a list
    data_exists = "data" in response and isinstance(response["data"], list)
    print_test_result(data_exists, "Response has data field with a list of reports")
    
    # Check if we got at least one report
    if data_exists:
        has_reports = len(response["data"]) > 0
        print_test_result(has_reports, f"Found reports matching the search term '{search_term}'")
        
        if has_reports:
            print(f"{Colors.OKBLUE}Found {len(response['data'])} reports matching '{search_term}'{Colors.ENDC}")
            
            # Print the names of the reports found
            report_names = [report["name"] for report in response["data"]]
            print(f"{Colors.OKBLUE}Reports found: {', '.join(report_names)}{Colors.ENDC}")
    
    return success_field and data_exists

def test_combined_filters() -> bool:
    """Test 7: Combined Filters - Test /api/reports?group=COMPRAS&search=stock"""
    print_test_header("Combined Filters")
    
    group = "COMPRAS"
    search_term = "stock"
    response = make_request("/reports", {"group": group, "search": search_term})
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a list
    data_exists = "data" in response and isinstance(response["data"], list)
    print_test_result(data_exists, "Response has data field with a list of reports")
    
    # Check if all reports belong to the specified group
    if data_exists and len(response["data"]) > 0:
        all_in_group = all(report["group"] == group for report in response["data"])
        print_test_result(all_in_group, f"All reports belong to the {group} group")
        
        # Check if all reports contain the search term (case insensitive)
        all_match_search = all(search_term.lower() in report["name"].lower() for report in response["data"])
        print_test_result(all_match_search, f"All reports contain the search term '{search_term}'")
        
        # Print the names of the reports found
        report_names = [report["name"] for report in response["data"]]
        print(f"{Colors.OKBLUE}Reports found: {', '.join(report_names)}{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}No reports found matching both group={group} and search={search_term}{Colors.ENDC}")
    
    return success_field and data_exists

def test_individual_report() -> bool:
    """Test 8: Individual Report - Test /api/reports/{report_id}"""
    print_test_header("Individual Report")
    
    # First, get all reports to extract a valid ID
    all_reports = make_request("/reports")
    
    if not all_reports.get("success", False) or "data" not in all_reports or len(all_reports["data"]) == 0:
        print_test_result(False, "Could not get a valid report ID to test")
        return False
    
    # Get the ID of the first report
    report_id = all_reports["data"][0]["id"]
    report_name = all_reports["data"][0]["name"]
    
    # Now test the individual report endpoint
    response = make_request(f"/reports/{report_id}")
    
    # Check if response has success field and it's true
    success_field = response.get("success", False)
    print_test_result(success_field, "Response has success field and it's true")
    
    # Check if data field exists and is a dictionary
    data_exists = "data" in response and isinstance(response["data"], dict)
    print_test_result(data_exists, "Response has data field with a report object")
    
    # Check if the report has the expected ID
    if data_exists:
        id_matches = response["data"]["id"] == report_id
        print_test_result(id_matches, f"Report ID matches the requested ID ({report_id})")
        
        # Print the report details
        print(f"{Colors.OKBLUE}Report details: {response['data']['name']} (Group: {response['data']['group']}){Colors.ENDC}")
    
    # Test with an invalid ID
    invalid_id = "invalid-id-12345"
    try:
        invalid_response = requests.get(f"{API_BASE_URL}/reports/{invalid_id}")
        # The API might return a JSON error instead of a 404 status code
        expected_error = invalid_response.status_code == 404 or (
            invalid_response.status_code == 200 and 
            "success" in invalid_response.json() and 
            not invalid_response.json()["success"]
        )
        print_test_result(expected_error, "Returns error for invalid report ID")
    except Exception as e:
        print_test_result(False, f"Error testing invalid ID: {str(e)}")
    
    return success_field and data_exists

def run_all_tests() -> None:
    """Run all tests and print a summary"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}===== POWER BI DIRECTORY API TESTS ====={Colors.ENDC}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Reports API", test_reports_api),
        ("Groups API", test_groups_api),
        ("Stats API", test_stats_api),
        ("Filtering by Group", test_filtering_by_group),
        ("Search Functionality", test_search_functionality),
        ("Combined Filters", test_combined_filters),
        ("Individual Report", test_individual_report)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.HEADER}===== TEST SUMMARY ====={Colors.ENDC}")
    all_passed = True
    for name, result in results.items():
        status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    # Print overall result
    print(f"\n{Colors.BOLD}Overall Result: ", end="")
    if all_passed:
        print(f"{Colors.OKGREEN}ALL TESTS PASSED{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}SOME TESTS FAILED{Colors.ENDC}")

if __name__ == "__main__":
    run_all_tests()