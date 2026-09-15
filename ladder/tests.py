from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from ladder.models import LadderGeneration


class LadderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "start": "1",
            "target": "2",
            "steps": 2,
            "window": 5,
        }

    def test_generation_is_persisted_for_the_current_session(self):
        result = [{"position": 0, "name": "Start"}]
        with patch("ladder.views.generate_ladder", return_value=(result, [])):
            response = self.client.post("/api/ladders/", self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["result"], result)
        self.assertEqual(LadderGeneration.objects.count(), 1)
        self.assertEqual(
            response.wsgi_request.session.session_key,
            LadderGeneration.objects.get().session_key,
        )

    def test_invalid_generation_request_returns_bad_request(self):
        response = self.client.post(
            "/api/ladders/",
            {**self.payload, "steps": 0},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("steps", response.data)

    def test_history_is_isolated_by_session(self):
        with patch(
            "ladder.views.generate_ladder",
            return_value=([{"position": 0, "name": "Start"}], []),
        ):
            self.client.post("/api/ladders/", self.payload, format="json")

        another_client = APIClient()
        response = another_client.get("/api/ladders/history/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
