#!/usr/bin/env python3
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

# 포트/해상도/프레임 조절
PORT = 8090
WIDTH, HEIGHT = 640, 480
FPS = 15   
JPEG_Q = 6     

FFMPEG_CMD = (
    f"rpicam-vid -t 0 --inline -n --width {WIDTH} --height {HEIGHT} --framerate 30 -o - "
    f"| ffmpeg -loglevel error -f h264 -i - -an -vf fps={FPS} -q:v {JPEG_Q} -f mjpeg -"
)

# rpicam+ffmpeg 프로세스 시작(파이프라인은 shell로)
PROC = subprocess.Popen(FFMPEG_CMD, shell=True, stdout=subprocess.PIPE, bufsize=0)

BOUNDARY = b"--frame\r\n"
HDR = b"Content-Type: image/jpeg\r\n\r\n"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/stream"):
            self.send_response(404)
            self.end_headers()
            return

        if self.path == "/":
            # 간단 HTML
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h2>MJPEG Stream</h2><img src='/stream' />")
            return

        # /stream : MJPEG 멀티파트 응답
        self.send_response(200)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Connection", "close")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.end_headers()

        try:
            buf = b""
            while True:
                chunk = PROC.stdout.read(4096)
                if not chunk:
                    break
                buf += chunk

                # JPEG 프레임 경계(FF D8 ... FF D9)로 잘라서 전송
                while True:
                    start = buf.find(b"\xff\xd8")
                    end = buf.find(b"\xff\xd9")
                    if start != -1 and end != -1 and end > start:
                        jpg = buf[start:end+2]
                        buf = buf[end+2:]

                        self.wfile.write(BOUNDARY)
                        self.wfile.write(HDR)
                        self.wfile.write(jpg)
                        self.wfile.write(b"\r\n")
                    else:
                        break
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *args):
        return

def main():
    httpd = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[OK] MJPEG server: http://0.0.0.0:{PORT}/  (stream: /stream)")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
