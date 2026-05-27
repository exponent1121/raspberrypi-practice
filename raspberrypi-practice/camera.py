import subprocess
from datetime import datetime
from pathlib import Path

OUT_DIR = Path("captures")
OUT_DIR.mkdir(exist_ok=True)

# 저장 파일명
out_path = OUT_DIR / "test.jpeg"

# 해상도 설정
WIDTH, HEIGHT = 1024, 768

cmd = [
    "rpicam-still",
    "-o", str(out_path),
    "--width", str(WIDTH),
    "--height", str(HEIGHT),
    "--nopreview",   
    "--timeout", "500" 
]

subprocess.run(cmd, check=True)
print(f"[OK] saved photo: {out_path}")
