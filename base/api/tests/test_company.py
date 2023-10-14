# from django.test import TestCase

import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class companyTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username="admin")
        # athenticate the user for every action
        self.client.force_authenticate(user=self.user)

    def test_creating_new_company(self):
        data = { "companyName" : "new company", "taxNumber" : 123456, "address" : "address" }
        response = self.client.post("/api/company/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_company(self):
        data = { "companyName" : "new company", "taxNumber" : 123456, "address" : "address" }
        new_data = { "companyName" : "updated name company", "taxNumber" : 1234569, "address" : "address 2" }

        response = self.client.post("/api/company/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        companyId = response.data["id"]

        # now test to update it
        response = self.client.put(
            f"/api/company/update/{companyId}", new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve and check if the new information is updated and if the updated version correspond to what was sent
        response = self.client.get(
            f"/api/company/list/{companyId}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["companyName"], new_data["companyName"])
        self.assertEqual(response.data["taxNumber"], new_data["taxNumber"])
        self.assertEqual(response.data["address"], new_data["address"])

    def test_delete_company(self):
        data = { "companyName" : "new company", "taxNumber" : 123456, "address" : "address" }

        response = self.client.post("/api/company/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        companyId = response.data["id"]

        # now test to update it
        response = self.client.delete(
            f"/api/company/delete/{companyId}")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
