from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, RequestFactory, TestCase

User = get_user_model()


class ClientsViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.specialist = User.objects.create_user(
            email="specialist@test.com",
            password="testpassword",
            is_superuser=True,
            is_specialist=True,
            is_staff=True
        )
        cls.client_user = User.objects.create_user(
            first_name="user_name",
            last_name="user_surname",
            email="client@test.com",
            password="testpassword",
        )

    def setUp(self):
        self.client = Client()
        self.client.force_login(ClientsViewSetTests.specialist)
        self.factory = RequestFactory()
        cache.clear()

    def test_api_client_create(self):
        request = self.factory.post(
            "/api/clients/",
            data={
                "user": {
                    "first_name": "string",
                    "last_name": "string",
                    "middle_name": "string",
                    "role": "0",
                    "email": "user@exa.com",
                    "phone_number": ")74)51815(28+)+",
                    "dob": "2023-10-18",
                    "gender": "0",
                    "params": {
                        "weight": 0,
                        "height": 0,
                        "waist_size": 0
                    },
                    "capture": "string"
                },
                "diseases": "string",
                "exp_diets": "string",
                "exp_trainings": "string",
                "bad_habits": "string",
                "notes": "string",
                "food_preferences": "string"
            },
            format="json",
        )
        view = ClientsViewSet.as_view({"get": "detail", "post": "create"})
        force_authenticate(request, user=ClientsViewSetTests.specialist)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpecialistClient.objects.count(), 2)