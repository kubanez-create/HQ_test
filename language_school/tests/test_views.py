import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.exceptions import (
    EmptyGroupListError,
    ObjectNotFoundError,
    UserAlreadyInProductError,
)
from products.models import Group, Product

User = get_user_model()


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.product = Product.objects.create(
            name="some_name",
            start_time="2024-03-02T13:08:09.265Z",
            cost=10000.15,
            author=self.user,
            max_students=5,
            min_students=2,
        )
        self.group = Group.objects.create(name="Name", product=self.product)
        self.url = f"/api/products/{self.product.id}/"

    def test_retrieve_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_not_found(self):
        response = self.client.get("/api/products/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grant_access_success(self):
        user_id = self.user.id
        data = {"user": user_id}
        response = self.client.post(
            f"{self.url}grant/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user in self.product.participants.all())

    def test_grant_access_user_not_found(self):
        data = {"user": 999}
        with self.assertRaisesMessage(
            ObjectNotFoundError, "Either the user or product doesn't exist."
        ):
            self.client.post(
                f"{self.url}grant/",
                data=json.dumps(data),
                content_type="application/json",
            )

    def test_grant_access_user_already_in_product(self):
        self.product.participants.add(self.user)
        data = {"user": self.user.id}
        with self.assertRaisesMessage(
            UserAlreadyInProductError,
            "User already has access to the product."
        ):
            self.client.post(
                f"{self.url}grant/",
                data=json.dumps(data),
                content_type="application/json",
            )

    def test_grant_access_empty_group_list_error(self):
        self.product.groups.all().delete()  # Delete all associated groups
        data = {"user": self.user.id}
        with self.assertRaisesMessage(
            EmptyGroupListError,
            (
                "Product doesn't seem to have any associated groups. "
                "Add at least one group, please."
            ),
        ):
            self.client.post(
                f"{self.url}grant/",
                data=json.dumps(data),
                content_type="application/json",
            )
