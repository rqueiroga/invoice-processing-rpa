from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

from reset_demo import reset

ROOT = Path(__file__).parent
URL = "http://127.0.0.1:8000"


def wait_for_server(timeout: float = 10) -> None:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urlopen(URL, timeout=0.5):
                return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("The demo server did not start.")


def main() -> int:
    print("Preparing a clean demo...")
    reset()

    server = subprocess.Popen(
        [sys.executable, str(ROOT / "demo_server.py")],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    try:
        wait_for_server()
        print(f"Demo systems: {URL}")
        print("Starting the automation...\n")

        result = subprocess.run([sys.executable, str(ROOT / "main.py")], cwd=ROOT, env=os.environ.copy())

        if result.returncode == 0:
            print("\nDemo completed. Results were written to data/invoice_queue.xlsx.")
            print(f"You can inspect the demo systems at {URL} before closing this window.")
        else:
            print("\nThe automation ended with an error. Check the messages above.")

        try:
            input("Press Enter to stop the demo server...")
        except EOFError:
            pass
        return result.returncode
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
