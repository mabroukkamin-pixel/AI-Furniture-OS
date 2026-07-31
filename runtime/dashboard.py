import argparse
import socket
import threading
import webbrowser
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def _dashboard_is_running(host, port):
    try:
        with urlopen(
            (
                f"http://{host}:{port}"
                "/system/readiness"
            ),
            timeout=1
        ) as response:
            return response.status == 200
    except (
        OSError,
        URLError
    ):
        return False


def _port_is_in_use(host, port):
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as connection:
        return (
            connection.connect_ex(
                (
                    host,
                    port
                )
            )
            == 0
        )


def _open_dashboard(host, port):
    webbrowser.open(
        f"http://{host}:{port}/dashboard"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Start the AI Furniture OS dashboard"
        )
    )

    parser.add_argument(
        "--host",
        default=DEFAULT_HOST
    )

    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT
    )

    parser.add_argument(
        "--no-browser",
        action="store_true"
    )

    args = parser.parse_args()

    dashboard_url = (
        f"http://{args.host}:{args.port}"
        "/dashboard"
    )

    if _dashboard_is_running(
        args.host,
        args.port
    ):
        print(
            "AI Furniture OS is already running:"
        )
        print(
            dashboard_url
        )

        if not args.no_browser:
            webbrowser.open(
                dashboard_url
            )

        return

    if _port_is_in_use(
        args.host,
        args.port
    ):
        parser.error(
            (
                f"Port {args.port} is already in use "
                "by another application."
            )
        )

    if not args.no_browser:
        timer = threading.Timer(
            1.5,
            _open_dashboard,
            args=(
                args.host,
                args.port
            )
        )

        timer.daemon = True
        timer.start()

    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=False
    )


if __name__ == "__main__":
    main()