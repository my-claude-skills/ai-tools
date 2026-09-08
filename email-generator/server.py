#!/usr/bin/env python3
"""
Email Template Generator - local server.

Serves the app (index.html) and stores templates in templates.json in this
same folder, so your templates are a real file you can share, copy to another
computer, and commit to git.

Run it:
    Windows : double-click start.bat   (or:  py server.py)
    Mac/Linux: ./start.sh              (or:  python3 server.py)

Then open http://127.0.0.1:8770/index.html (start.bat/start.sh do this for you).
Stop it with Ctrl+C.
"""
import http.server
import socketserver
import json
import os
import sys
import threading
import webbrowser
from urllib.parse import urlparse

DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(DIR, "templates.json")
PORT = int(os.environ.get("ETG_PORT", "8770"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/api/templates":
            try:
                with open(TEMPLATES, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except FileNotFoundError:
                data = []
            except Exception as e:
                return self._json(500, {"error": str(e)})
            return self._json(200, data)
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path == "/api/templates":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                data = json.loads(raw)
                assert isinstance(data, list), "expected a JSON array"
            except Exception as e:
                return self._json(400, {"error": "invalid payload: %s" % e})
            try:
                # Keep a rolling backup, then write atomically so a crash can't corrupt the file.
                if os.path.exists(TEMPLATES):
                    try:
                        os.replace(TEMPLATES, TEMPLATES + ".bak")
                    except Exception:
                        pass
                tmp = TEMPLATES + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                os.replace(tmp, TEMPLATES)
            except Exception as e:
                return self._json(500, {"error": str(e)})
            return self._json(200, {"ok": True, "count": len(data)})
        return self._json(404, {"error": "not found"})

    def log_message(self, *args):
        pass  # keep the console quiet


def main():
    os.chdir(DIR)
    url = "http://127.0.0.1:%d/index.html" % PORT
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
            print("=" * 60)
            print(" Email Template Generator is running.")
            print(" Open:  " + url)
            print(" Templates file:  " + TEMPLATES)
            print(" Press Ctrl+C to stop.")
            print("=" * 60)
            threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nStopped.")
    except OSError as e:
        print("Could not start on port %d (%s)." % (PORT, e))
        print("It may already be running. Try opening: " + url)
        print("Or set a different port, e.g.  set ETG_PORT=8780  (Windows)  then run again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
