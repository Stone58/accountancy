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

    def test_creating_new_operation_type(self):
        data = {"operationType": "new type"}
        response = self.client.post("/api/operationtype/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_operation_type(self):
        data = {"operationType": "new type"}
        new_data = {"operationType": "updated type"}

        response = self.client.post("/api/operationtype/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        operationTypeId = response.data["id"]

        # now test to update it
        response = self.client.put(
            f"/api/operationtype/update/{operationTypeId}", new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve and check if the new information is updated and if the updated version correspond to what was sent
        response = self.client.get(
            f"/api/operationtype/list/{operationTypeId}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["operationType"], new_data["operationType"])

    def test_delete_operation_type(self):
        data = {"operationType": "new type"}

        response = self.client.post("/api/operationtype/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # take the id of the tested created new user
        operationTypeId = response.data["id"]

        # now test to update it
        response = self.client.delete(
            f"/api/operationtype/delete/{operationTypeId}")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
