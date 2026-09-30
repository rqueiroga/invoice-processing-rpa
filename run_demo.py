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
    raise RuntimeError("O servidor da demonstração não iniciou.")


def main() -> int:
    print("Preparando uma demonstração limpa...")
    reset()

    server = subprocess.Popen(
        [sys.executable, str(ROOT / "demo_server.py")],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    try:
        wait_for_server()
        print(f"Sistemas da demonstração: {URL}")
        print("Iniciando a automação...\n")

        result = subprocess.run([sys.executable, str(ROOT / "main.py")], cwd=ROOT, env=os.environ.copy())

        if result.returncode == 0:
            print("\nDemonstração concluída. Os resultados foram gravados em data/invoice_queue.xlsx.")
            print(f"Você pode conferir os sistemas em {URL} antes de fechar esta janela.")
        else:
            print("\nA automação terminou com erro. Confira as mensagens acima.")

        try:
            input("Pressione Enter para encerrar o servidor da demonstração...")
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
