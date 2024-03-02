from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from products.models import Product
from products.validators import validate_start_time

User = get_user_model()


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="testauthor", password="testpassword"
        )

    def test_validate_start_time_future(self):
        future_start_time = timezone.now() + timezone.timedelta(days=1)
        product = Product(
            name="Test Product",
            start_time=future_start_time,
            cost=50.0,
            author=self.author,
            max_students=10,
            min_students=5,
        )

        try:
            validate_start_time(product.start_time)
        except ValidationError:
            self.fail("Validation error raised for a future start time")

    def test_validate_start_time_past_time(self):
        past_start_time = timezone.now() - timezone.timedelta(days=1)
        product = Product(
            name="Test Product",
            start_time=past_start_time,
            cost=50.0,
            author=self.author,
            max_students=10,
            min_students=5,
        )

        with self.assertRaises(ValidationError) as context:
            validate_start_time(product.start_time)

        self.assertEqual(
            str(context.exception), "['Start time must be in the future.']"
        )
