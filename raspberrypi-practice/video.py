import subprocess
from datetime import datetime
from pathlib import Path

OUT_DIR = Path("captures")
OUT_DIR.mkdir(exist_ok=True)

# 저장 파일명(시간 포함)
out_path = OUT_DIR / "test.h264"

# 촬영 설정
SECONDS = 10
WIDTH, HEIGHT = 1280, 720
FPS = 30

cmd = [
    "rpicam-vid",
    "-o", str(out_path),
    "--width", str(WIDTH),
    "--height", str(HEIGHT),
    "--framerate", str(FPS),
    "-t", str(SECONDS * 1000),  # ms 단위
    "--nopreview"
]

subprocess.run(cmd, check=True)
print(f"[OK] saved video: {out_path}")
