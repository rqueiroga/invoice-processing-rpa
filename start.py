from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REQUIREMENTS = ROOT / "requirements.txt"
SETUP_MARKER = VENV / ".setup_hash"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def requirements_hash() -> str:
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()


def ensure_environment() -> None:
    if not VENV_PYTHON.exists():
        print("Primeira execução: criando o ambiente Python local...")
        run([sys.executable, "-m", "venv", str(VENV)])

    current_hash = requirements_hash()
    installed_hash = SETUP_MARKER.read_text(encoding="utf-8").strip() if SETUP_MARKER.exists() else ""

    if installed_hash == current_hash:
        return

    print("Instalando as dependências do projeto...")
    run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS)])

    print("Instalando o navegador Chromium do Playwright...")
    run([str(VENV_PYTHON), "-m", "playwright", "install", "chromium"])

    SETUP_MARKER.write_text(current_hash, encoding="utf-8")
    print("Configuração concluída.\n")


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inicia a demonstração do RPA de processamento de notas")
    parser.add_argument("--pt", action="store_true", help="abre a interface da demonstração em português")
    parser.add_argument("--speed", type=int, default=600, help="intervalo entre ações do navegador em milissegundos")
    return parser.parse_args()


def main() -> int:
    options = args()

    try:
        ensure_environment()
    except subprocess.CalledProcessError as exc:
        print(f"\nA configuração falhou com o código {exc.returncode}.")
        return exc.returncode

    env = os.environ.copy()
    env["DEMO_LANG"] = "pt" if options.pt else "en"
    env["DEMO_SPEED_MS"] = str(max(0, options.speed))

    print("Iniciando a demonstração...\n")
    result = subprocess.run(
        [str(VENV_PYTHON), str(ROOT / "run_demo.py")],
        cwd=ROOT,
        env=env,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
