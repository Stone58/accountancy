# from django.test import TestCase

import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class operationTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username="admin")
        # athenticate the user for every action
        self.client.force_authenticate(user=self.user)

        company = {"companyName": "new company",
                   "taxNumber": 123456, "address": "address"}
        response = self.client.post("/api/company/create", company)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.company_id = response.data["id"]

        operationType = {"operationType": "new operation"}
        response = self.client.post(
            "/api/operationtype/create", operationType)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.operationType_id = response.data["id"]

    def test_creating_new_operation(self):
        data = {"quantity": "123.00000", "company": self.company_id,
                "operationType": self.operationType_id}
        response = self.client.post("/api/operation/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_operation(self):
        data = {"quantity": 123.00000, "company": self.company_id,
                "operationType": self.operationType_id}
        new_data = {"quantity": 125025, "company": self.company_id,
                "operationType": self.operationType_id}
        
        response = self.client.post("/api/operation/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        operationId = response.data["id"]

        # now test to update it
        response = self.client.put(
            f"/api/operation/update/{operationId}", new_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve and check if the new information is updated and if the updated version correspond to what was sent
        response = self.client.get(
            f"/api/operation/list/{operationId}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(float(response.data["quantity"]), new_data["quantity"])
        self.assertEqual(response.data["operationType"], new_data["operationType"])
        self.assertEqual(response.data["company"], new_data["company"])

    def test_delete_operation(self):
        data = {"quantity": 123.00000, "company": self.company_id,
                "operationType": self.operationType_id}

        response = self.client.post("/api/operation/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new operation
        operationId = response.data["id"]

        # now test to update it
        response = self.client.delete(
            f"/api/operation/delete/{operationId}")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
