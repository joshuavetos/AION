import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT / ".venv"
PYTHON = sys.executable


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.check_call(cmd, cwd=cwd)


def ensure_python() -> None:
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11+ is required")


def ensure_venv() -> None:
    if not VENV_DIR.exists():
        run([PYTHON, "-m", "venv", str(VENV_DIR)])


def install_python_deps() -> None:
    pip = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "pip"
    run([str(pip), "install", "-r", "aiond/requirements.txt"])


def install_node_deps() -> None:
    run(["npm", "install"], cwd=ROOT / "app")


def main() -> None:
    ensure_python()
    ensure_venv()
    install_python_deps()
    install_node_deps()
    print("SYSTEM READY. RUN: npm run dev")


if __name__ == "__main__":
    main()
