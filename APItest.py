import unittest
import requests
from faker import Faker

class PythonAPIs(unittest.TestCase):
    fake = Faker()
    baseUrl = "https://deployment.api-python.boilerplate.hng.tech"
    valid_body = {"email": fake.email(), "password": "Pa$$w0rd!", "first_name": fake.first_name(), "last_name": fake.last_name()}
    existing_body = {"email": "woss5@mailinator.com", "password": "Pa$$w0rd!", "first_name": fake.first_name(), "last_name": fake.last_name()}
    invalid_body = {"email": 12345678, "password": "Pa$$w0rd!", "first_name": 10110111, "last_name": fake.last_name()}
    valid_body1 = {"email": fake.email(), "password": "Pa$$w0rd!", "first_name": fake.first_name(), "last_name": fake.last_name()}
    valid_body2 = {"email": fake.email(), "password": "Pa$$w0rd!", "first_name": fake.first_name(), "last_name": fake.last_name()}
    change_password = {"old_password": "Pa$$w0rd!", "new_password": "Pa$$w0rd!!"}
    create_profile = {"username": fake.user_name(), "pronouns": "It/is", "job_title": "Tester", "department": "Science", "social": "@me", "bio": fake.paragraph(), "phone_number": "+2348026653321", "avatar_url": fake.image_url(), "recovery_email": fake.email()}
    success_message = "Successfully fetched items"
    success_message = "Blog post retrieved successfully!"
    blog_id = None
    invalid_blog_id = "invalid-blog-id"
    error_message = "Post not found"
    valid_comment_body = {"content": "blogcomment"}
    invalid_comment_body = {"content": 1234323}
    empty_comment_body = {"content": ""}
    comment = "Comment added successfully!"
    update_blog_body = {"title": "new_title", "content": "updated_content"}
    empty_content_body = {"title": "new_title", "content": ""}
    invalid_content_body = {"title": 12343, "content": 12342}
    no_content_error_message = "Title and content cannot be empty"
    invalid_body_error_message = "Invalid input"
    access_token = None
    user_id = None
    user_email = None
    super_token = None
    super_id = None
    super_email = None

    @classmethod
    def setUpClass(cls):
        # cls.user_email = None
        # cls.access_token = None
        # cls.user_id = None
        register_body = {"email": cls.fake.email(), "password": "Pa$$w0rd!", "first_name": cls.fake.first_name(), "last_name": cls.fake.last_name()}
        register_response = requests.post(f"{cls.baseUrl}/api/v1/auth/register", json = register_body)
        register_response_data = register_response.json()
        # print(register_response_data)

        cls.access_token = register_response_data["data"]["access_token"]
        cls.user_id = register_response_data["data"]["user"]["id"]

    #  Register User endpoint 
    def test_01_register_user_successfully(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register", json = self.valid_body2)
        self.assertEqual(response.status_code, 201, "Expected status code 201, got {}".format(response.status_code))
        response_data = response.json()
        self.assertIn("access_token", response_data["data"])
        self.assertIsInstance(response_data["data"]["access_token"], str)
        self.assertGreater(len(response_data["data"]["access_token"]), 0)
        user_data = response_data["data"]["user"]
        self.__class__.user_email = user_data["email"]
        self.__class__.user_id = user_data["id"]
        self.__class__.access_token = response_data['data']['access_token']
        # print(response_data)
        print(f"Email: {self.__class__.user_email}, Access Token: {self.__class__.access_token}, User ID: {self.__class__.user_id}")
        print("\nUser successfully created, status code is {}".format(response.status_code))

    def test_register_with_invalid_credentials(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register", json = self.invalid_body)
        self.assertEqual(response.status_code, 422, "Expected status code 422, got {}".format(response.status_code))
        # response_data = response.json()
        # self.assertEqual(response_data.get("error"), "Invalid credentials")
        print("\nInvalid user credentials detected, status code is {}".format(response.status_code))

    def test_register_with_existing_credentials(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register", json = self.existing_body)
        self.assertEqual(response.status_code, 400, "Expected status code 400, got {}".format(response.status_code))
        # response_data = response.json()
        # self.assertEqual(response_data.get("error"), "Invalid credentials")
        print("\nExisting user credentials detected, status code is {}".format(response.status_code))

    #  Logout endpoint
    def test_logout(self):
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        # print(self.access_token)
        response = requests.post(f"{self.baseUrl}/api/v1/auth/logout", headers = headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        print("\nUser / Super Admin logged out successfully, status code is {}".format(response.status_code))

    def test_token_expiry(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register", json = self.valid_body1)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        access_token = response_data["data"]["access_token"]
        import jwt
        decoded_token = jwt.decode(access_token, options = {"verify_signature": False})
        self.assertIn("exp", decoded_token)
        self.assertGreater(decoded_token["exp"], 0)  # To ensure 'exp' has a positive value
        print("\nThe token expires in {}".format(decoded_token["exp"]))

    #  Register Super Admin endpoint
    def test_04_register_admin_successfully(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register-super-admin", json = self.valid_body)
        self.assertEqual(response.status_code, 201, "Expected status code 201, got {}".format(response.status_code))
        response_data = response.json()
        self.assertIn("access_token", response_data["data"])
        self.assertIsInstance(response_data["data"]["access_token"], str)
        self.assertGreater(len(response_data["data"]["access_token"]), 0)
        super_data = response_data["data"]["user"]
        self.__class__.super_email = super_data["email"]
        self.__class__.super_id = super_data["id"]
        self.__class__.super_token = response_data['data']['access_token']
        # print(response_data)
        print(f"Admin Email: {self.__class__.super_email}, Admin Token: {self.__class__.super_token}, Admin ID: {self.__class__.super_id}")
        print("\nSuper Admin successfully created, status code is {}".format(response.status_code))

    def test_register_admin_with_invalid_credentials(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register-super-admin", json = self.invalid_body)
        self.assertEqual(response.status_code, 422, "Expected status code 422, got {}".format(response.status_code))
        # response_data = response.json()
        # self.assertEqual(response_data.get("error"), "Invalid credentials")
        print("\nInvalid admin credentials detected, status code is {}".format(response.status_code))

    def test_register_admin_with_existing_credentials(self):
        response = requests.post(f"{self.baseUrl}/api/v1/auth/register-super-admin", json = self.existing_body)
        self.assertEqual(response.status_code, 400, "Expected status code 400, got {}".format(response.status_code))
        # response_data = response.json()
        # self.assertEqual(response_data.get("error"), "Invalid credentials")
        print("\nExisting admin credentials detected, status code is {}".format(response.status_code))

    #  Refresh token endpoint
    def test_refresh_token(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        response = requests.post(f"{self.baseUrl}/api/v1/auth/refresh-access-token", headers = headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        print("\nAccess token refreshed successfully, status code is {}".format(response.status_code))

    #  Refresh endpoint
    # def test_refresh_token(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/auth/refresh-access-token", headers = headers)
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nToken refreshed successfully, status code is {}".format(response.status_code))

    #  Send token(OTP) by email endpoint
    # def test_send_token(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/auth/request-token", json = {"email": "woss@mailinator.com"})
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nToken sent to user email successfully, status code is {}".format(response.status_code))

    #  Login with token(OTP) endpoint
    # def test_login_with_token(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/auth/verify-token", json = {"email": "woss@mailinator.com", "token": "123456"})
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nToken sent to user email has been used to login successfully, status code is {}".format(response.status_code))

    #  Request Magic Link endpoint
    # def test_request_magicLink(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/auth/request-magic-link", json = {"email": "woss@mailinator.com"})
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nMagic link request successful, status code is {}".format(response.status_code))

    #  Facebook Login endpoint
    # def test_facebook_login(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/auth/facebook-login", json = {"token": self.access_token})
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nFacebook login successful, status code is {}".format(response.status_code))

    #  Newsletter subscription endpoint
    # def test_newsletter(self):
    #     headers = {
    #         "Authorization": f"Bearer {self.__class__.access_token}"
    #     }
    #     response = requests.post(f"{self.baseUrl}/api/v1/newsletters", json = {"email": "woss@mailinator.com"}, headers = headers)
    #     self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
    #     print("\nEmail successfully subscribed to the Newsletter, status code is {}".format(response.status_code))

    def test_change_password(self):
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        response = requests.patch(f"{self.baseUrl}/api/v1/users/me/password", json = self.change_password, headers = headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        print("\nPassword changed successfully, status code is {}".format(response.status_code))

    def test_get_admin_data(self):
        headers = {
            "Authorization": f"Bearer {self.__class__.super_token}"
        }
        response = requests.get(f"{self.baseUrl}/api/v1/auth/admin", headers = headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, admin!'})
        print('Admin Data read successfully!', "status_code: ", response.status_code)

    def test_get_auth_google_redirect_success(self):
        response = requests.get(f"{self.baseUrl}/api/v1/auth/google")
        self.assertEqual(response.status_code, 200)
        print('Google Auth Redirect successful!', "status_code: ", response.status_code)

    def test_get_current_user_details(self):
        headers = {
            "Authorization": f"Bearer {self.__class__.access_token}"
        }
        response = requests.get(f"{self.baseUrl}/api/v1/users/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        print('User Data read successfully!', "status_code: ", response.status_code)

    def test_17_delete_user(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        response = requests.delete(f"{self.baseUrl}/api/v1/users/{self.__class__.user_id}", headers=headers)
        self.assertEqual(response.status_code, 204)
        print('User deleted successfully!', "status_code: ", response.status_code)

    def test_03_get_current_user_profile(self):
        headers = {
            "Authorization": f"Bearer {self.__class__.access_token}"
        }
        response = requests.get(f"{self.baseUrl}/api/v1/profile/current-user", headers=headers)
        self.assertEqual(response.status_code, 201)
        # print(response.json())
        print('User Profile Data read successfully!, status code is {}'.format(response.status_code))

    def test_02_create_profile(self):
        headers = {"Authorization": f"Bearer {self.__class__.access_token}"}
        fake1 =Faker()
        response = requests.post(f"{self.baseUrl}/api/v1/profile/", json = {"username": fake1.user_name(), "pronouns": "It/is", "job_title": "Tester", "department": "Dub", "social": "@me", "bio": "This is a test.", "phone_number": "+2348026683339", "avatar_url": fake1.image_url(), "recovery_email": fake1.email()}, headers = headers)
        # print(response.json())
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        print("\nProfile created successfully, status code is {}".format(response.status_code))

    def test_get_all_organization_billing_plans(self):
        headers = {
            "Authorization": f"Bearer {self.__class__.access_token}"
        }
        response = requests.get(f"{self.baseUrl}/api/v1/organization/billing-plans", headers = headers)
        self.assertEqual(response.status_code, 200)
        # print(response.json())
        print('Organization Billing Data read successfully!', "status_code: ", response.status_code)

    def test_06_get_all_blogs(self):
        headers = {
            "Authorization": f"Bearer {self.__class__.super_token}"
        }
        response = requests.get(f"{self.baseUrl}/api/v1/blogs/", headers=headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        response_data = response.json()
        self.assertIn("success", response_data)
        self.assertEqual(response_data["success"], True)
        # self.assertEqual(response_data["message"], self.success_message)
        self.assertIsInstance(response_data["data"]["items"][0]["author_id"], str)
        self.assertIsInstance(response_data["data"]["items"][0]["id"], str)
        self.assertIsInstance(response_data["data"]["items"][0]["updated_at"], str)
        # print(response_data)
        print("\nAll blogs fetched successfully, status code is {}".format(response.status_code)) 

    def test_05_create_blog(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        fake2 =Faker()
        response = requests.post(f"{self.baseUrl}/api/v1/blogs/", json = {"title": "Test blog", "content": "lorem ipsum or something", "image_url": fake2.image_url(), "tags": ["fiction?"], "excerpt": "I'm tired"}, headers = headers)
        # print(response.json())
        response_data = response.json()
        self.__class__.blog_id = response_data['data']['id']
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        print("\nBlog created successfully, status code is {}".format(response.status_code))

    def test_07_get_blog_by_id(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        response = requests.get(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}", headers=headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        response_data = response.json()
        self.assertIn("success", response_data)
        self.assertEqual(response_data["message"], self.success_message)
        self.assertIsInstance(response_data["data"]["author_id"], str)
        self.assertIsInstance(response_data["data"]["id"], str)
        self.assertIsInstance(response_data["data"]["updated_at"], str)
        print("\nBlog post retrieved successfully, status code is {}".format(response.status_code)) 
    
    def test_get_blog_by_invalid_id(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        response = requests.get(f"{self.baseUrl}/api/v1/blogs/{self.invalid_blog_id}", headers=headers)
        self.assertIn(response.status_code, {400, 422}, "Expected status code 400/422, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["success"], False)
        self.assertEqual(response_data["message"], self.error_message)
        self.assertIn(response_data["status_code"], {400, 422})
        print("\nGet Blog by invalid ID test successful, status code is {}".format(response.status_code))

    def test_add_comment_with_valid_credentials(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        response = requests.post(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}/comments", json = self.valid_comment_body, headers=headers)
        self.assertEqual(response.status_code, 201, "Expected status code 201, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["message"], self.comment)
        self.assertIn("content", response_data["data"])
        self.assertIsInstance(response_data["data"]["blog_id"], str)
        self.assertIsInstance(response_data["data"]["id"], str)
        self.assertIsInstance(response_data["data"]["created_at"], str)
        self.assertEqual(response_data["data"]["blog_id"], self.blog_id)
        print("\nComment Added successfully, status code is {}".format(response.status_code))
        
    def test_add_comment_with_invalid_credentials(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}        
        response = requests.post(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}/comments", json = self.invalid_comment_body, headers=headers)
        self.assertEqual(response.status_code, 422, "Expected status code 422, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["errors"][0]["msg"], "Input should be a valid string")
        print("\nInvalid attempt to add comments test successful, status code is {}".format(response.status_code))
    
    def test_add_comment_with_empty_credentials(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}        
        response = requests.post(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}/comments", json = self.empty_comment_body, headers=headers)
        self.assertEqual(response.status_code, 422, "Expected status code 422, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["errors"][0]["msg"], "String should have at least 1 character")
        print("\nAttempt to add comments with no value test successful, status code is {}".format(response.status_code))   

    def test_update_blog(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        
        response = requests.put(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}", json=self.update_blog_body, headers=headers)
        self.assertEqual(response.status_code, 200, "Expected status code 200, got {}".format(response.status_code))
        response_data = response.json()
        # self.assertEqual(response_data["message"], self.success_message)
        self.assertEqual(response_data["success"], True)
        self.assertIsInstance(response_data["data"]["author_id"], str)
        self.assertIsInstance(response_data["data"]["id"], str)
        self.assertIsInstance(response_data["data"]["updated_at"], str)
        print("\nBlog post updated successfully, status code is {}".format(response.status_code))
    
    def test_update_blog_with_invalid_blog_id(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        
        response = requests.put(f"{self.baseUrl}/api/v1/blogs/{self.invalid_blog_id}", json=self.update_blog_body, headers=headers)
        self.assertEqual(response.status_code, 404, "Expected status code 404, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["message"], self.error_message)
        self.assertEqual(response_data["success"], False)
        self.assertEqual(response_data["status_code"], 404)
        
        print("\nAttempt to update blog with an invalid blog ID test Successful, status code is {}".format(response.status_code))
    
    def test_update_blog_with_empty_content(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        
        response = requests.put(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}", json=self.empty_content_body, headers=headers)
        self.assertEqual(response.status_code, 400, "Expected status code 400, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["message"], self.no_content_error_message)
        self.assertEqual(response_data["success"], False)
        self.assertEqual(response_data["status_code"], 400)
        
        print("\nBlog post updated successfully, status code is {}".format(response.status_code)) 
    
    
    def test_update_blog_with_invalid_body(self):
        headers = {"Authorization": f"Bearer {self.__class__.super_token}"}
        
        response = requests.put(f"{self.baseUrl}/api/v1/blogs/{self.blog_id}", json=self.invalid_content_body, headers=headers)
        self.assertEqual(response.status_code, 422, "Expected status code 422, got {}".format(response.status_code))
        response_data = response.json()
        self.assertEqual(response_data["message"], self.invalid_body_error_message)
        self.assertEqual(response_data["success"], False)
        self.assertEqual(response_data["status_code"], 422)
        self.assertEqual(response_data["errors"][0]["msg"], "Input should be a valid string")
        
        print("\nBlog post updated successfully, status code is {}".format(response.status_code))


if __name__ == "__main__":
    unittest.main()