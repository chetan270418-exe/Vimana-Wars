"""
build_exe.py
Automated script to bundle Vimana Wars into a standalone Windows/Mac/Linux executable.
Ready for publishing on itch.io or Steam.

Usage:
  python build_exe.py
"""
import os
import subprocess
import sys
from pathlib import Path


def build():
    print("==================================================")
    print("   Vimana Wars — Standalone Executable Builder    ")
    print("==================================================")

    # Check if pyinstaller is installed
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("\nInstalling PyInstaller in virtualenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    dist_dir = Path("dist")
    sep = os.pathsep

    # Command arguments for PyInstaller
    # Bundles assets, sounds, fonts, and dependencies into a clean release folder
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",             # directory distribution (fast startup, easy modding)
        "--windowed",           # hide black console window
        "--name=VimanaWars",
        f"--add-data=assets{sep}assets",
        f"--add-data=constants.py{sep}.",
        f"--add-data=CREDITS.md{sep}.",
        f"--add-data=README.md{sep}.",
        "main.py",
    ]

    print(f"\nRunning PyInstaller build command:\n{' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("🎉 BUILD SUCCESSFUL!")
        print("Your game executable is ready in:")
        print(f"  {dist_dir.resolve() / 'VimanaWars'}")
        print("To test: run dist/VimanaWars/VimanaWars.exe")
        print("To publish: zip the 'dist/VimanaWars' folder and upload to itch.io!")
        print("=" * 50)
    else:
        print("\n❌ Build failed. Please check error logs above.")


if __name__ == "__main__":
    build()
