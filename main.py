from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import webbrowser


ROOT = Path(__file__).resolve().parent


class AppHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "text/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Pиріжки.lab mobile PWA locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Use 0.0.0.0 for phone testing.")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve the app on.")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the app in a browser.")
    args = parser.parse_args()

    handler = partial(AppHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}/"

    print(f"Пиріжки.lab app is running: {url}")
    print("Press Ctrl+C to stop.")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
