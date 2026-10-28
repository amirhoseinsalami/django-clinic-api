
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from rest_framework.test import APIClient

from .models import DoctorProfile, Speciality


User = get_user_model()


def response_items(response):
    """Handle either a paginated or unpaginated API response."""
    data = response.json()

    if isinstance(data, dict) and "results" in data:
        return data["results"]

    return data


class DoctorCacheTests(TestCase):

    def setUp(self):
        cache.clear()

        self.client = APIClient()

        self.patient = User.objects.create_user(
            username="cache_patient",
            password="test-password",
            role=User.Role.PATIENT,
        )
        self.client.force_authenticate(user=self.patient)

        self.speciality = Speciality.objects.create(
            name="Cardiology"
        )

        self.doctor_user = User.objects.create_user(
            username="cache_doctor",
            password="test-password",
            role=User.Role.DOCTOR,
            first_name="Alex",
            last_name="Doctor",
        )

        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            bio="Test doctor",
            experienced_years=10,
            consultation_fee=Decimal("100.00"),
            is_verified=True,
        )

        self.doctor.specialities.add(self.speciality)

        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_specialities_list_uses_cached_data(self):
        with CaptureQueriesContext(connection) as first_queries:
            first_response = self.client.get("/api/specialities/")

        self.assertEqual(first_response.status_code, 200)

        self.assertTrue(
            any(
                "doctors_speciality" in query["sql"].lower()
                for query in first_queries.captured_queries
            ),
            "The first request should query the speciality table.",
        )

        with CaptureQueriesContext(connection) as second_queries:
            second_response = self.client.get("/api/specialities/")

        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(
            any(
                item["name"] == "Cardiology"
                for item in response_items(second_response)
            )
        )

        self.assertFalse(
            any(
                "doctors_speciality" in query["sql"].lower()
                for query in second_queries.captured_queries
            ),
            "The second request should use cached data.",
        )

    def test_saving_speciality_invalidates_cached_data(self):
        self.client.get("/api/specialities/")

        cache_key = "clinic:specialities:v1"
        self.assertIsNotNone(cache.get(cache_key))

        self.speciality.name = "Neurology"
        self.speciality.save()

        self.assertIsNone(cache.get(cache_key))

        response = self.client.get("/api/specialities/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                item["name"] == "Neurology"
                for item in response_items(response)
            )
        )

    def test_doctors_list_uses_cached_response(self):
        with CaptureQueriesContext(connection) as first_queries:
            first_response = self.client.get("/api/doctors/")

        self.assertEqual(first_response.status_code, 200)

        self.assertTrue(
            any(
                "doctors_doctorprofile" in query["sql"].lower()
                for query in first_queries.captured_queries
            ),
            "The first request should query the doctor table.",
        )

        with CaptureQueriesContext(connection) as second_queries:
            second_response = self.client.get("/api/doctors/")

        self.assertEqual(second_response.status_code, 200)

        self.assertFalse(
            any(
                "doctors_doctorprofile" in query["sql"].lower()
                for query in second_queries.captured_queries
            ),
            "The second request should use the cached response.",
        )

    def test_saving_doctor_invalidates_cached_response(self):
        first_response = self.client.get("/api/doctors/")

        self.assertEqual(first_response.status_code, 200)

        first_doctor = next(
            item
            for item in response_items(first_response)
            if item["id"] == self.doctor.id
        )

        self.assertEqual(
            Decimal(str(first_doctor["consultation_fee"])),
            Decimal("100.00"),
        )

        self.doctor.consultation_fee = Decimal("250.00")
        self.doctor.save()

        second_response = self.client.get("/api/doctors/")

        self.assertEqual(second_response.status_code, 200)

        updated_doctor = next(
            item
            for item in response_items(second_response)
            if item["id"] == self.doctor.id
        )

        self.assertEqual(
            Decimal(str(updated_doctor["consultation_fee"])),
            Decimal("250.00"),
        )
