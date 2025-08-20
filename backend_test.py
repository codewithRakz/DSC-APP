import requests
import sys
import json
from datetime import datetime

class DSCBackendTester:
    def __init__(self, base_url="http://localhost:8001"):

        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.created_member_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        return self.run_test("Health Check", "GET", "api/health", 200)

    def test_root_endpoint(self):
        """Test root endpoint"""
        return self.run_test("Root Endpoint", "GET", "", 200)

    def test_club_info(self):
        """Test club info endpoint"""
        return self.run_test("Club Info", "GET", "api/club-info", 200)

    def test_get_empty_team_members(self):
        """Test getting team members when empty"""
        return self.run_test("Get Team Members (Empty)", "GET", "api/team-members", 200)

    def test_create_team_member(self):
        """Test creating a team member"""
        test_member = {
            "name": "Test Member",
            "role": "Test Role",
            "photo": "https://example.com/photo.jpg",
            "description": "This is a test member for API testing"
        }
        
        success, response = self.run_test(
            "Create Team Member", 
            "POST", 
            "api/team-members", 
            200, 
            data=test_member
        )
        
        if success and 'id' in response:
            self.created_member_id = response['id']
            print(f"   Created member with ID: {self.created_member_id}")
            return True
        return False

    def test_get_team_members_with_data(self):
        """Test getting team members when data exists"""
        return self.run_test("Get Team Members (With Data)", "GET", "api/team-members", 200)

    def test_get_single_team_member(self):
        """Test getting a single team member"""
        if not self.created_member_id:
            print("❌ Skipped - No member ID available")
            return False
            
        return self.run_test(
            "Get Single Team Member", 
            "GET", 
            f"api/team-members/{self.created_member_id}", 
            200
        )

    def test_update_team_member(self):
        """Test updating a team member"""
        if not self.created_member_id:
            print("❌ Skipped - No member ID available")
            return False
            
        update_data = {
            "name": "Updated Test Member",
            "role": "Updated Test Role",
            "description": "This member has been updated via API testing"
        }
        
        return self.run_test(
            "Update Team Member", 
            "PUT", 
            f"api/team-members/{self.created_member_id}", 
            200, 
            data=update_data
        )

    def test_delete_team_member(self):
        """Test deleting a team member"""
        if not self.created_member_id:
            print("❌ Skipped - No member ID available")
            return False
            
        return self.run_test(
            "Delete Team Member", 
            "DELETE", 
            f"api/team-members/{self.created_member_id}", 
            200
        )

    def test_get_nonexistent_member(self):
        """Test getting a non-existent team member"""
        fake_id = "non-existent-id-12345"
        return self.run_test(
            "Get Non-existent Member", 
            "GET", 
            f"api/team-members/{fake_id}", 
            404
        )

    def test_update_nonexistent_member(self):
        """Test updating a non-existent team member"""
        fake_id = "non-existent-id-12345"
        update_data = {"name": "Should Fail"}
        
        return self.run_test(
            "Update Non-existent Member", 
            "PUT", 
            f"api/team-members/{fake_id}", 
            404, 
            data=update_data
        )

    def test_delete_nonexistent_member(self):
        """Test deleting a non-existent team member"""
        fake_id = "non-existent-id-12345"
        return self.run_test(
            "Delete Non-existent Member", 
            "DELETE", 
            f"api/team-members/{fake_id}", 
            404
        )

    def test_create_invalid_member(self):
        """Test creating a team member with invalid data"""
        invalid_member = {
            "role": "Missing Name Field"
            # Missing required 'name' field
        }
        
        return self.run_test(
            "Create Invalid Member", 
            "POST", 
            "api/team-members", 
            422,  # Validation error
            data=invalid_member
        )

def main():
    print("🚀 Starting DSC Backend API Tests")
    print("=" * 50)
    
    tester = DSCBackendTester()
    
    # Run all tests in sequence
    test_methods = [
        tester.test_root_endpoint,
        tester.test_health_check,
        tester.test_club_info,
        tester.test_get_empty_team_members,
        tester.test_create_team_member,
        tester.test_get_team_members_with_data,
        tester.test_get_single_team_member,
        tester.test_update_team_member,
        tester.test_delete_team_member,
        tester.test_get_nonexistent_member,
        tester.test_update_nonexistent_member,
        tester.test_delete_nonexistent_member,
        tester.test_create_invalid_member
    ]
    
    for test_method in test_methods:
        try:
            test_method()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        failed_tests = tester.tests_run - tester.tests_passed
        print(f"⚠️  {failed_tests} test(s) failed. Backend needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())