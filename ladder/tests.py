from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
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
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.data["count"], 0)

    def test_history_is_paginated(self):
        session_key = self.client.session.session_key
        if not session_key:
            self.client.session.create()
            session_key = self.client.session.session_key
        LadderGeneration.objects.bulk_create(
            [
                LadderGeneration(
                    session_key=session_key,
                    start="1",
                    target="2",
                    steps=2,
                    window=5,
                    result=[],
                )
                for _ in range(3)
            ]
        )

        response = self.client.get("/api/ladders/history/?page_size=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["next"], 2)

    def test_csrf_endpoint_sets_cookie(self):
        response = self.client.get("/api/csrf/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)

    def test_generation_requires_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        with patch("ladder.views.generate_ladder", return_value=([], [])):
            response = client.post("/api/ladders/", self.payload, format="json")

        self.assertEqual(response.status_code, 403)

    def test_generation_accepts_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        csrf_response = client.get("/api/csrf/")
        csrf_token = csrf_response.cookies[settings.CSRF_COOKIE_NAME].value

        with patch("ladder.views.generate_ladder", return_value=([], [])):
            response = client.post(
                "/api/ladders/",
                self.payload,
                format="json",
                HTTP_X_CSRFTOKEN=csrf_token,
            )

        self.assertEqual(response.status_code, 201)

    def test_health_check_reports_ok(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    @override_settings(HISTORY_MAX_PER_SESSION=2)
    def test_history_is_trimmed_to_the_configured_limit(self):
        with patch(
            "ladder.views.generate_ladder",
            return_value=([{"position": 0, "name": "Start"}], []),
        ):
            for _ in range(3):
                self.client.post("/api/ladders/", self.payload, format="json")

        self.assertEqual(
            LadderGeneration.objects.filter(
                session_key=self.client.session.session_key
            ).count(),
            2,
        )

    @override_settings(HISTORY_RETENTION_DAYS=1)
    def test_history_excludes_expired_records_on_get(self):
        session_key = self.client.session.session_key
        if not session_key:
            self.client.session.create()
            session_key = self.client.session.session_key
        old_generation = LadderGeneration.objects.create(
            session_key=session_key,
            start="1",
            target="2",
            steps=2,
            window=5,
            result=[],
        )
        LadderGeneration.objects.filter(pk=old_generation.pk).update(
            created_at=timezone.now() - timedelta(days=2)
        )

        response = self.client.get("/api/ladders/history/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
