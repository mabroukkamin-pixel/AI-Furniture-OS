import unittest
from unittest.mock import patch

from runtime.dashboard import main


class DashboardLauncherTests(unittest.TestCase):

    @patch(
        "runtime.dashboard.uvicorn.run"
    )
    @patch(
        "runtime.dashboard.webbrowser.open"
    )
    @patch(
        "runtime.dashboard._dashboard_is_running",
        return_value=True,
    )
    def test_opens_existing_dashboard(
        self,
        dashboard_is_running,
        browser_open,
        uvicorn_run,
    ):
        with patch(
            "sys.argv",
            ["dashboard"],
        ):
            main()

        dashboard_is_running.assert_called_once_with(
            "127.0.0.1",
            8000
        )

        browser_open.assert_called_once_with(
            "http://127.0.0.1:8000/dashboard"
        )

        uvicorn_run.assert_not_called()

    @patch(
        "runtime.dashboard.uvicorn.run"
    )
    @patch(
        "runtime.dashboard._port_is_in_use",
        return_value=False,
    )
    @patch(
        "runtime.dashboard._dashboard_is_running",
        return_value=False,
    )
    def test_starts_server_when_port_is_free(
        self,
        dashboard_is_running,
        port_is_in_use,
        uvicorn_run,
    ):
        with patch(
            "sys.argv",
            [
                "dashboard",
                "--no-browser",
            ],
        ):
            main()

        dashboard_is_running.assert_called_once_with(
            "127.0.0.1",
            8000
        )

        port_is_in_use.assert_called_once_with(
            "127.0.0.1",
            8000
        )

        uvicorn_run.assert_called_once_with(
            "api.main:app",
            host="127.0.0.1",
            port=8000,
            reload=False
        )


if __name__ == "__main__":
    unittest.main()