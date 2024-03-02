import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from products.models import Product
from api.views import ProductViewSet

User = get_user_model()

class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.product = Product.objects.create(
            name="some_name",
            start_time="2024-03-02T13:08:09.265Z",
            cost=10000.15,
            author=self.user,
            max_students=5,
            min_students=2,)
        self.url = f"/api/products/{self.product.id}/"

    def test_retrieve_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("api.views.get_object_or_404")
    def test_retrieve_product_not_found(self, mock_get_object_or_404):
        mock_get_object_or_404.side_effect = ObjectDoesNotExist()
        response = self.client.get("/api/products/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("api.views.get_object_or_404")
    def test_grant_access_success(self, mock_get_object_or_404):
        user_id = self.user.id
        data = {"user": user_id}
        response = self.client.post(f"{self.url}grant/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user in self.product.participants.all())

    @patch("api.views.get_object_or_404")
    def test_grant_access_user_not_found(self, mock_get_object_or_404):
        data = {"user": 999}
        response = self.client.post(f"{self.url}grant/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("api.views.get_object_or_404")
    def test_grant_access_user_already_in_product(self, mock_get_object_or_404):
        self.product.participants.add(self.user)
        data = {"user": self.user.id}
        response = self.client.post(f"{self.url}grant/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User already has access to the product.", response.data["detail"])

    @patch("api.views.get_object_or_404")
    @patch("api.views.distribute_students")
    def test_grant_access_empty_group_list_error(self, mock_distribute_students, mock_get_object_or_404):
        self.product.groups.all().delete()  # Delete all associated groups
        data = {"user": self.user.id}
        response = self.client.post(f"{self.url}grant/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Product doesn't seem to have any associated groups.", response.data["detail"])
