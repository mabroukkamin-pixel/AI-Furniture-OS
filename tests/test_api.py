import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class ApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def make_result(self, generation_status):
        return {
            "product": "Partition001",
            "generation": {
                "status": generation_status,
                "output_folder": (
                    "outputs/Partition001"
                ),
            },
            "prompt": {
                "length": 100
            },
        }

    def test_home_is_running(self):
        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "running"
        )

    def test_success_returns_http_200(self):
        with patch(
            "api.main.run",
            return_value=self.make_result(
                "success"
            ),
        ):
            response = self.client.post(
                "/generate",
                json={
                    "product_id": "Partition001"
                },
            )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "succeeded"
        )

    def test_local_mode_returns_http_503(self):
        with patch(
            "api.main.run",
            return_value=self.make_result(
                "local_only"
            ),
        ):
            response = self.client.post(
                "/generate",
                json={
                    "product_id": "Partition001"
                },
            )

        self.assertEqual(
            response.status_code,
            503
        )

        self.assertEqual(
            response.json()["status"],
            "failed"
        )

    def test_engine_failure_returns_http_502(self):
        with patch(
            "api.main.run",
            return_value=self.make_result(
                "error"
            ),
        ):
            response = self.client.post(
                "/generate",
                json={
                    "product_id": "Partition001"
                },
            )

        self.assertEqual(
            response.status_code,
            502
        )

        self.assertEqual(
            response.json()["status"],
            "failed"
        )


if __name__ == "__main__":
    unittest.main()