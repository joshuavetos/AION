import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and handle errors."""
    try:
        print(f"🚀 Running: {command}")
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        sys.exit(1)

def main():
    root_dir = Path(__file__).resolve().parent.parent
    backend_dir = root_dir / "backend"
    app_dir = root_dir / "app"

    print("🔧 Bootstrapping Slop Drop (PromptForge)...")

    # 1. Setup Python Backend
    print("\n🐍 Setting up Backend...")
    if not (backend_dir / "venv").exists():
        run_command(f"{sys.executable} -m venv venv", cwd=backend_dir)
    
    # Install Python dependencies
    pip_cmd = "venv\\Scripts\\pip" if platform.system() == "Windows" else "venv/bin/pip"
    run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir)

    # 2. Setup Node.js Frontend
    print("\n⚛️ Setting up Frontend...")
    if (app_dir / "package.json").exists():
        run_command("npm install", cwd=app_dir)
    else:
        print("⚠️ No package.json found in app/. Skipping npm install.")

    print("\n✅ System Ready!")
    print("👉 To start the backend: cd backend && source venv/bin/activate && python -m server.main")
    print("👉 To start the frontend: cd app && npm run dev")

if __name__ == "__main__":
    main()
