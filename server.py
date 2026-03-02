#!/usr/bin/env python3
"""Simple server to serve GLB viewer UI and handle CSV saving."""

import http.server
import json
import os
import csv
from pathlib import Path
from urllib.parse import urlparse

PORT = 8080
BASE_DIR = Path(__file__).parent.resolve()
GLBS_DIR = BASE_DIR / "glbs"
CSV_PATH = BASE_DIR / "labels.csv"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/glbs":
            self._send_json(self._list_glbs())
        elif parsed.path == "/api/labels":
            self._send_json(self._read_labels())
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/labels":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            self._write_labels(body)
            self._send_json({"status": "ok"})
        else:
            self.send_error(404)

    def _list_glbs(self):
        files = sorted(f.name for f in GLBS_DIR.glob("*.glb"))
        return files

    def _read_labels(self):
        labels = {}
        if CSV_PATH.exists():
            with open(CSV_PATH, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    labels[row["id"]] = int(row["label"])
        return labels

    def _write_labels(self, labels: dict):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "label"])
            writer.writeheader()
            for glb_id, label in sorted(labels.items()):
                writer.writerow({"id": glb_id, "label": label})

    def _send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # quieter logging
        pass


if __name__ == "__main__":
    print(f"Starting GLB Viewer at http://localhost:{PORT}")
    server = http.server.HTTPServer(("", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
