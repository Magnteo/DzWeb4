from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import socket
from urllib.parse import parse_qs
from UDP_server import func_UDP_soket
from threading import Thread


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            decoded_data = post_data.decode("utf-8")

            parsed = parse_qs(decoded_data)
            parsed_dict = {
                "username": parsed.get("username", [""])[0],
                "message": parsed.get("message", [""])[0],
            }

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            json_string = json.dumps(parsed_dict)

            sock.sendto(json_string.encode("utf-8"), ("localhost", 5000))
            sock.close()

            self.send_response(302)
            self.send_header("Location", "/message")
            self.end_headers()

    def do_GET(self):
        if self.path.startswith("/static"):
            file_path = Path(self.path.lstrip("/"))
            if file_path.exists():
                if file_path.suffix == ".css":
                    content_type = "text/css"
                elif file_path.suffix == ".png":
                    content_type = "image/png"
                else:
                    content_type = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(file_path.read_bytes())
                return
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write("Файл не знайдено".encode("utf-8"))
                return
        if self.path == "/":
            file_path = Path("index.html")
            code = 200
        elif self.path == "/message":
            file_path = Path("message.html")
            code = 200
        else:
            file_path = Path("error.html")
            code = 404
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            self.send_response(code)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("index.html не знайдено".encode("utf-8"))


udp_thread = Thread(target=func_UDP_soket, daemon=True)
udp_thread.start()

server = HTTPServer(("localhost", 3000), MyHandler)
print("HTTP сервер запущено на http://localhost:3000")
server.serve_forever()
