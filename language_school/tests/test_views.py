from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from language_school.products.views import ProductViewSet


User = get_user_model()


class ProductTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tutor = User.objects.create_user(
            username="tutor",
            password="testpassword",
            is_superuser=True,
        )
        cls.client_user = User.objects.create_user(
            username="user_name",
            password="testpassword",
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(ProductTest.tutor)
        self.factory = APIRequestFactory()
        cache.clear()

    def test_api_client_create(self):
        request = self.factory.post(
            "/api/product/grant",
            data={
                "user": 1,
                "product": 1
            },
            format="json",
        )
        view = ProductViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ProductTest.tutor)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
