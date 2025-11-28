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
NPM_EXECUTABLE = shutil.which("npm")


def ensure_python():
    if PYTHON_EXECUTABLE is None:
        print("Python 3.11 is required but not found in PATH", file=sys.stderr)
        sys.exit(1)

    version_output = subprocess.check_output([PYTHON_EXECUTABLE, "--version"], text=True).strip()
    if not version_output.startswith("Python 3.11"):
        print(f"Expected Python 3.11, found: {version_output}", file=sys.stderr)
        sys.exit(1)


def create_venv():
    if not VENV_PATH.exists():
        subprocess.check_call([PYTHON_EXECUTABLE, "-m", "venv", str(VENV_PATH)])
    pip_path = VENV_PATH / "bin" / "pip"
    subprocess.check_call([str(pip_path), "install", "--upgrade", "pip"])
    subprocess.check_call([str(pip_path), "install", "-r", str(REQUIREMENTS_PATH)])


def install_frontend_dependencies():
    if NPM_EXECUTABLE is None:
        print("npm is required to install frontend dependencies", file=sys.stderr)
        sys.exit(1)

    try:
        node_version = subprocess.check_output(["node", "--version"], text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js is required to install frontend dependencies", file=sys.stderr)
        sys.exit(1)

    major_version = int(node_version.lstrip("v").split(".")[0])
    if major_version < 18:
        print(f"Node.js 18+ is required, found: {node_version}", file=sys.stderr)
        sys.exit(1)

    subprocess.check_call(["npm", "install"], cwd=APP_DIR)


def main():
    ensure_python()
    create_venv()
    install_frontend_dependencies()
    print("SYSTEM READY. RUN: npm run dev")


if __name__ == "__main__":
    main()
