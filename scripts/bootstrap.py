#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_EXECUTABLE = shutil.which("python3.11")
VENV_PATH = REPO_ROOT / ".venv"
REQUIREMENTS_PATH = REPO_ROOT / "aiond" / "requirements.txt"
APP_DIR = REPO_ROOT / "app"


def ensure_python():
    if PYTHON_EXECUTABLE is None:
        print("Python 3.11 is required but not found in PATH", file=sys.stderr)
        sys.exit(1)


def create_venv():
    if not VENV_PATH.exists():
        subprocess.check_call([PYTHON_EXECUTABLE, "-m", "venv", str(VENV_PATH)])
    pip_path = VENV_PATH / "bin" / "pip"
    subprocess.check_call([str(pip_path), "install", "-r", str(REQUIREMENTS_PATH)])


def install_frontend_dependencies():
    subprocess.check_call(["npm", "install"], cwd=APP_DIR)


def main():
    ensure_python()
    create_venv()
    install_frontend_dependencies()
    print("SYSTEM READY. RUN: npm run dev")


if __name__ == "__main__":
    main()
