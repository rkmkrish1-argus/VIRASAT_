"""
One-Click Application Launcher (Cross-Platform Python Version)
Dr. B.R. Ambedkar Digital Heritage Archive (PS 26096)
Ministry of Social Justice & Empowerment (MoSJE)
"""

import sys
import os
import time
import urllib.request
import webbrowser
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def check_server_health(port=8000) -> bool:
    try:
        url = f"http://127.0.0.1:{port}/api/health"
        req = urllib.request.urlopen(url, timeout=1)
        return req.getcode() == 200
    except Exception:
        return False

def main():
    print("=" * 65)
    print(" DR. B.R. AMBEDKAR DIGITAL HERITAGE ARCHIVE (PS 26096)")
    print(" Ministry of Social Justice & Empowerment (MoSJE)")

    print("=" * 65)
    print()

    os.chdir(PROJECT_ROOT)

    # Check if server is already running
    if check_server_health(8000):
        print("[*] Archive engine is already running on http://127.0.0.1:8000")
    else:
        venv_py = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
        python_bin = str(venv_py) if venv_py.exists() else sys.executable
        uvicorn_cmd = [python_bin, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", "8000"]
        subprocess.Popen(uvicorn_cmd, cwd=str(PROJECT_ROOT))

        print("[*] Waiting for server health check...", end="", flush=True)
        for _ in range(15):
            time.sleep(1)
            print(".", end="", flush=True)
            if check_server_health(8000):
                print("\n[✓] Archive Engine initialized successfully!")
                break
        else:
            print("\n[!] Warning: Server startup took longer than expected. Attempting to open browser...")

    print()
    print("=" * 65)
    print(" Archive Server Live: http://127.0.0.1:8000")
    print(" - Student Access Passcode: {STUDENT}")
    print(" - Researcher Access Passcode: RESEARCHER")
    print("=" * 65)
    print()

    time.sleep(0.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
