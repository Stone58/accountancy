# from django.test import TestCase

import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class UserTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username="admin")

    def test_creating_new_user(self):
        data = {"password": "newPassword", "username": "accountant",
                "email": "accountant@admin.com", "is_active": True, "group": [2]}

        # authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/user/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        data = {"password": "newPassword", "username": "accountant",
                "email": "accountant@admin.com", "is_active": True, "group": [2]}
        new_data = {"username": "new_accountant",
                    "email": "accountant@admin.com", "is_active": False}

        # authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/user/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        user_id = response.data["id"]

        # now test to update it
        response = self.client.put(f"/api/user/update/{user_id}", new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve and check if the new information is updated and if the updated version correspond to what was sent
        response = self.client.get(f"/api/user/list/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], new_data["username"])
        self.assertEqual(response.data["email"], new_data["email"])
        self.assertEqual(response.data["is_active"], new_data["is_active"])

    def test_update_user(self):
        data = {"password": "newPassword", "username": "accountant",
                "email": "accountant@admin.com", "is_active": True, "group": [2]}
        new_data = {"username": "new_accountant",
                    "email": "accountant@admin.com", "is_active": False}

        # authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/user/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        user_id = response.data["id"]

        # now test to update it
        response = self.client.put(f"/api/user/update/{user_id}", new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve and check if the new information is updated and if the updated version correspond to what was sent
        response = self.client.get(f"/api/user/list/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], new_data["username"])
        self.assertEqual(response.data["email"], new_data["email"])
        self.assertEqual(response.data["is_active"], new_data["is_active"])

    def test_update_user_password(self):
        data = {"password": "newPassword", "username": "accountant",
                "email": "accountant@admin.com", "is_active": True, "group": [2]}
        new_data = {"username": "new_accountant",
                    "email": "accountant@admin.com", "is_active": False}

        # authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/user/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_password = "newPassword"

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Update the user's password
        response = self.client.put(
            f"/api/user/updatepassword/{self.user.id}", {"new_password": new_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the password is updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertTrue(updated_user.check_password(new_password))

    def test_update_user_group(self):
        data = {"password": "newPassword", "username": "accountant",
                "email": "accountant@admin.com", "is_active": True, "group": [2]}

        # authenticate the user
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/user/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Update the user's password
        response = self.client.put(f"/api/user/updategroup/{self.user.id}/{3}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
