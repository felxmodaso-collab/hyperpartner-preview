#!/usr/bin/env python3
"""Tiny editor server for the FTE plates layout.
Serves the _deploy folder, plus:
  POST /save  -> writes raw JSON body to _fte-layout.json
  GET  /load  -> returns _fte-layout.json (or {})
Run: python _fte_editor_server.py   (port 8077)
"""
import http.server, socketserver, os

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYOUT = os.path.join(ROOT, "_fte-layout.json")
PORT = 8077

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        if self.path.split("?")[0] == "/save":
            n = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            with open(LAYOUT, "wb") as f:
                f.write(body)
            self.send_response(200); self.send_header("Content-Type", "application/json"); self._cors(); self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404); self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/load":
            try:
                with open(LAYOUT, "rb") as f:
                    data = f.read()
            except FileNotFoundError:
                data = b"{}"
            self.send_response(200); self.send_header("Content-Type", "application/json"); self._cors(); self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), H) as httpd:
    print(f"FTE editor server on http://127.0.0.1:{PORT}/_fte-editor.html")
    httpd.serve_forever()
