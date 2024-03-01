from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import ProductViewSet
from products.models import Product


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
        cls.product = Product.objects.create(
            name="some_name",
            start_time="2024-03-02T13:08:09.265Z",
            cost=10000.15,
            author=cls.tutor,
            max_students=5,
            min_students=2,
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(ProductTest.tutor)
        self.factory = APIRequestFactory()
        cache.clear()

    def test_participant_create(self):
        request = self.factory.post(
            f"/api/products/{ProductTest.product.id}/grant",
            data={"user": 1},
            format="json",
        )
        view = ProductViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ProductTest.tutor)
        response = view(request)
        print(ProductTest.product, ProductTest.product.id)
        print(response, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
