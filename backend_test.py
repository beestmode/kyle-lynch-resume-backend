#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Kyle Lynch Resume Application
Tests all FastAPI endpoints including authentication, CRUD operations, and PDF generation
"""

import requests
import json
import os
from datetime import datetime
import uuid

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://parchment-resume.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ResumeAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, message="", data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                data = response.json()
                if "Kyle Lynch Resume API" in data.get("message", ""):
                    self.log_test("Health Check", True, "API is running and healthy")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_get_resume(self):
        """Test getting resume data"""
        try:
            response = self.session.get(f"{API_BASE}/resume")
            if response.status_code == 200:
                data = response.json()
                # Check for required fields
                required_fields = ["personal_info", "highlights", "experience", "education", "skills"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Verify Kyle Lynch's data
                    personal_info = data.get("personal_info", {})
                    if "Kyle" in personal_info.get("name", "") and "kclynch@uh.edu" in personal_info.get("email", ""):
                        self.log_test("Get Resume Data", True, "Resume data retrieved successfully with correct personal info")
                        return True
                    else:
                        self.log_test("Get Resume Data", False, f"Personal info doesn't match expected Kyle Lynch data: {personal_info}")
                        return False
                else:
                    self.log_test("Get Resume Data", False, f"Missing required fields: {missing_fields}")
                    return False
            else:
                self.log_test("Get Resume Data", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Resume Data", False, f"Error: {str(e)}")
            return False
    
    def test_login(self):
        """Test admin login"""
        try:
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.auth_token = data["access_token"]
                    # Set authorization header for future requests
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    self.log_test("Admin Login", True, "Successfully logged in as admin")
                    return True
                else:
                    self.log_test("Admin Login", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_test("Admin Login", False, f"Status code: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Admin Login", False, f"Error: {str(e)}")
            return False
    
    def test_verify_token(self):
        """Test token verification"""
        if not self.auth_token:
            self.log_test("Token Verification", False, "No auth token available")
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/auth/verify")
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "username" in data.get("data", {}):
                    self.log_test("Token Verification", True, "Token verified successfully")
                    return True
                else:
                    self.log_test("Token Verification", False, f"Invalid verification response: {data}")
                    return False
            else:
                self.log_test("Token Verification", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Token Verification", False, f"Error: {str(e)}")
            return False
    
    def test_contact_form(self):
        """Test contact form submission"""
        try:
            contact_data = {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "subject": "Test Contact Message",
                "message": "This is a test message to verify the contact form functionality.",
                "recipient_email": "kclynch@uh.edu"
            }
            
            response = self.session.post(f"{API_BASE}/contact", json=contact_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "message_id" in data.get("data", {}):
                    self.log_test("Contact Form Submission", True, "Contact form submitted successfully")
                    return data["data"]["message_id"]
                else:
                    self.log_test("Contact Form Submission", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Contact Form Submission", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Contact Form Submission", False, f"Error: {str(e)}")
            return False
    
    def test_get_experiences(self):
        """Test getting work experiences"""
        try:
            response = self.session.get(f"{API_BASE}/resume/experience")
            if response.status_code == 200:
                data = response.json()
                if "experiences" in data and isinstance(data["experiences"], list):
                    # Check if Carlton Staffing is present (current position)
                    carlton_found = any("Carlton Staffing" in exp.get("company", "") for exp in data["experiences"])
                    if carlton_found:
                        self.log_test("Get Experiences", True, f"Retrieved {len(data['experiences'])} experiences including Carlton Staffing")
                        return data["experiences"]
                    else:
                        self.log_test("Get Experiences", True, f"Retrieved {len(data['experiences'])} experiences (Carlton Staffing not found)")
                        return data["experiences"]
                else:
                    self.log_test("Get Experiences", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_test("Get Experiences", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Experiences", False, f"Error: {str(e)}")
            return False
    
    def test_add_experience(self):
        """Test adding new work experience (requires auth)"""
        if not self.auth_token:
            self.log_test("Add Experience", False, "No auth token available")
            return False
            
        try:
            new_experience = {
                "position": "Test Position",
                "company": "Test Company",
                "location": "Test City, TX",
                "duration": "1/25 - 2/25",
                "description": "This is a test experience entry for API testing purposes.",
                "current": False,
                "achievements": ["Test achievement 1", "Test achievement 2"],
                "sort_order": 999
            }
            
            response = self.session.post(f"{API_BASE}/resume/experience", json=new_experience)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "id" in data.get("data", {}):
                    exp_id = data["data"]["id"]
                    self.log_test("Add Experience", True, f"Experience added successfully with ID: {exp_id}")
                    return exp_id
                else:
                    self.log_test("Add Experience", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Add Experience", False, f"Status code: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Add Experience", False, f"Error: {str(e)}")
            return False
    
    def test_update_experience(self, exp_id):
        """Test updating work experience (requires auth)"""
        if not self.auth_token or not exp_id:
            self.log_test("Update Experience", False, "No auth token or experience ID available")
            return False
            
        try:
            update_data = {
                "description": "Updated test experience description for API testing.",
                "achievements": ["Updated achievement 1", "Updated achievement 2", "New achievement 3"]
            }
            
            response = self.session.put(f"{API_BASE}/resume/experience/{exp_id}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Experience", True, "Experience updated successfully")
                    return True
                else:
                    self.log_test("Update Experience", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Update Experience", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Experience", False, f"Error: {str(e)}")
            return False
    
    def test_delete_experience(self, exp_id):
        """Test deleting work experience (requires auth)"""
        if not self.auth_token or not exp_id:
            self.log_test("Delete Experience", False, "No auth token or experience ID available")
            return False
            
        try:
            response = self.session.delete(f"{API_BASE}/resume/experience/{exp_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Delete Experience", True, "Experience deleted successfully")
                    return True
                else:
                    self.log_test("Delete Experience", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Delete Experience", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Delete Experience", False, f"Error: {str(e)}")
            return False
    
    def test_get_education(self):
        """Test getting education entries"""
        try:
            response = self.session.get(f"{API_BASE}/resume/education")
            if response.status_code == 200:
                data = response.json()
                if "education" in data and isinstance(data["education"], list):
                    # Check for expected education entries
                    pvamu_found = any("Prairie View A&M" in edu.get("institution", "") for edu in data["education"])
                    if pvamu_found:
                        self.log_test("Get Education", True, f"Retrieved {len(data['education'])} education entries including Prairie View A&M")
                        return data["education"]
                    else:
                        self.log_test("Get Education", True, f"Retrieved {len(data['education'])} education entries")
                        return data["education"]
                else:
                    self.log_test("Get Education", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_test("Get Education", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Education", False, f"Error: {str(e)}")
            return False
    
    def test_add_education(self):
        """Test adding new education entry (requires auth)"""
        if not self.auth_token:
            self.log_test("Add Education", False, "No auth token available")
            return False
            
        try:
            new_education = {
                "degree": "Test Certification",
                "institution": "Test University",
                "location": "Test City, TX",
                "duration": "1/25 - 2/25",
                "sort_order": 999
            }
            
            response = self.session.post(f"{API_BASE}/resume/education", json=new_education)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "id" in data.get("data", {}):
                    edu_id = data["data"]["id"]
                    self.log_test("Add Education", True, f"Education added successfully with ID: {edu_id}")
                    return edu_id
                else:
                    self.log_test("Add Education", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Add Education", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Add Education", False, f"Error: {str(e)}")
            return False
    
    def test_update_education(self, edu_id):
        """Test updating education entry (requires auth)"""
        if not self.auth_token or not edu_id:
            self.log_test("Update Education", False, "No auth token or education ID available")
            return False
            
        try:
            update_data = {
                "degree": "Updated Test Certification",
                "location": "Updated Test City, TX"
            }
            
            response = self.session.put(f"{API_BASE}/resume/education/{edu_id}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Education", True, "Education updated successfully")
                    return True
                else:
                    self.log_test("Update Education", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Update Education", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Education", False, f"Error: {str(e)}")
            return False
    
    def test_delete_education(self, edu_id):
        """Test deleting education entry (requires auth)"""
        if not self.auth_token or not edu_id:
            self.log_test("Delete Education", False, "No auth token or education ID available")
            return False
            
        try:
            response = self.session.delete(f"{API_BASE}/resume/education/{edu_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Delete Education", True, "Education deleted successfully")
                    return True
                else:
                    self.log_test("Delete Education", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Delete Education", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Delete Education", False, f"Error: {str(e)}")
            return False
    
    def test_update_personal_info(self):
        """Test updating personal information (requires auth)"""
        if not self.auth_token:
            self.log_test("Update Personal Info", False, "No auth token available")
            return False
            
        try:
            # Test with partial update
            update_data = {
                "phone": "713.226.9038",
                "location": "Houston, TX"
            }
            
            response = self.session.put(f"{API_BASE}/resume/personal-info", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Personal Info", True, "Personal info updated successfully")
                    return True
                else:
                    self.log_test("Update Personal Info", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Update Personal Info", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Personal Info", False, f"Error: {str(e)}")
            return False
    
    def test_update_highlights(self):
        """Test updating professional highlights (requires auth)"""
        if not self.auth_token:
            self.log_test("Update Highlights", False, "No auth token available")
            return False
            
        try:
            update_data = {
                "highlights": [
                    "Experienced Facilities Coordinator with extensive background in building automation, HVAC systems, and technical infrastructure management",
                    "Twenty years' experience in facilities operations, customer service coordination, and multi-system technical support across educational, corporate, and airport environments",
                    "Test highlight added via API testing"
                ]
            }
            
            response = self.session.put(f"{API_BASE}/resume/highlights", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Highlights", True, "Highlights updated successfully")
                    return True
                else:
                    self.log_test("Update Highlights", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Update Highlights", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Highlights", False, f"Error: {str(e)}")
            return False
    
    def test_update_skills(self):
        """Test updating skills list (requires auth)"""
        if not self.auth_token:
            self.log_test("Update Skills", False, "No auth token available")
            return False
            
        try:
            update_data = {
                "skills": [
                    "Facilities Coordination & Management",
                    "Building Automation Systems", 
                    "HVAC Operations & Maintenance",
                    "Customer Service & Liaison Relations",
                    "API Testing & Quality Assurance"
                ]
            }
            
            response = self.session.put(f"{API_BASE}/resume/skills", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Update Skills", True, "Skills updated successfully")
                    return True
                else:
                    self.log_test("Update Skills", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Update Skills", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Update Skills", False, f"Error: {str(e)}")
            return False
    
    def test_pdf_generation(self):
        """Test PDF generation"""
        try:
            response = self.session.get(f"{API_BASE}/resume/download-pdf")
            
            if response.status_code == 200:
                # Check if response is PDF
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    pdf_size = len(response.content)
                    self.log_test("PDF Generation", True, f"PDF generated successfully ({pdf_size} bytes)")
                    return True
                else:
                    self.log_test("PDF Generation", False, f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_test("PDF Generation", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("PDF Generation", False, f"Error: {str(e)}")
            return False
    
    def test_get_contact_messages(self):
        """Test getting contact messages (requires auth)"""
        if not self.auth_token:
            self.log_test("Get Contact Messages", False, "No auth token available")
            return False
            
        try:
            response = self.session.get(f"{API_BASE}/admin/contact-messages")
            
            if response.status_code == 200:
                data = response.json()
                if "messages" in data and isinstance(data["messages"], list):
                    self.log_test("Get Contact Messages", True, f"Retrieved {len(data['messages'])} contact messages")
                    return data["messages"]
                else:
                    self.log_test("Get Contact Messages", False, f"Invalid response format: {data}")
                    return False
            else:
                self.log_test("Get Contact Messages", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Contact Messages", False, f"Error: {str(e)}")
            return False
    
    def test_logout(self):
        """Test logout endpoint"""
        try:
            response = self.session.post(f"{API_BASE}/auth/logout")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    # Clear auth token
                    self.auth_token = None
                    self.session.headers.pop("Authorization", None)
                    self.log_test("Logout", True, "Logged out successfully")
                    return True
                else:
                    self.log_test("Logout", False, f"Invalid response: {data}")
                    return False
            else:
                self.log_test("Logout", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Logout", False, f"Error: {str(e)}")
            return False
    
    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        # Clear auth token temporarily
        original_token = self.auth_token
        self.auth_token = None
        self.session.headers.pop("Authorization", None)
        
        try:
            # Test protected endpoint without auth
            response = self.session.post(f"{API_BASE}/resume/experience", json={
                "position": "Test",
                "company": "Test",
                "location": "Test",
                "duration": "Test",
                "description": "Test"
            })
            
            if response.status_code == 401:
                self.log_test("Unauthorized Access Protection", True, "Protected endpoint correctly requires authentication")
                success = True
            else:
                self.log_test("Unauthorized Access Protection", False, f"Expected 401, got {response.status_code}")
                success = False
                
            # Restore auth token
            if original_token:
                self.auth_token = original_token
                self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                
            return success
        except Exception as e:
            self.log_test("Unauthorized Access Protection", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Kyle Lynch Resume Backend API Tests")
        print(f"📍 Testing API at: {API_BASE}")
        print("=" * 60)
        
        # Basic connectivity and data tests
        self.test_health_check()
        self.test_get_resume()
        
        # Authentication tests
        self.test_login()
        self.test_verify_token()
        
        # Contact form test (no auth required)
        message_id = self.test_contact_form()
        
        # Experience CRUD tests (require auth)
        experiences = self.test_get_experiences()
        exp_id = self.test_add_experience()
        if exp_id:
            self.test_update_experience(exp_id)
            self.test_delete_experience(exp_id)
        
        # Education CRUD tests (require auth)
        education = self.test_get_education()
        edu_id = self.test_add_education()
        if edu_id:
            self.test_update_education(edu_id)
            self.test_delete_education(edu_id)
        
        # Resume update tests (require auth)
        self.test_update_personal_info()
        self.test_update_highlights()
        self.test_update_skills()
        
        # PDF generation test
        self.test_pdf_generation()
        
        # Admin features test
        self.test_get_contact_messages()
        
        # Security tests
        self.test_unauthorized_access()
        
        # Logout test
        self.test_logout()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        failed = len(self.test_results) - passed
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
        return passed, failed

def main():
    """Main test execution"""
    tester = ResumeAPITester()
    tester.run_all_tests()
    
    # Return exit code based on results
    passed, failed = tester.print_summary()
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())