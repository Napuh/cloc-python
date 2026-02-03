from __future__ import annotations

import importlib.resources as resources
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_perl_available() -> bool:
    """Check if Perl is available on the system (required for Unix systems)."""
    return shutil.which("perl") is not None


def get_cloc_path() -> Path:
    """Get the path to the bundled cloc binary for the current platform."""
    current_platform = platform.system()

    # Determine the correct binary name for the platform
    binary_name = "cloc-2.08.exe" if current_platform == "Windows" else "cloc-2.08.pl"

    try:
        # For Python 3.9+
        if hasattr(resources, "files"):
            cloc_ref = resources.files("cloc_python") / binary_name

            with cloc_ref.open("rb") as src:
                temp_dir = tempfile.mkdtemp()
                temp_path = Path(temp_dir) / binary_name
                temp_path.write_bytes(src.read())

            os.chmod(temp_path, 0o755)

            return temp_path
        else:
            # Python 3.8 compatibility
            with resources.path("cloc_python", binary_name) as p:
                return p

    except (ImportError, AttributeError):
        # Fallback to using __file__
        module_dir = Path(__file__).parent
        return module_dir / binary_name


def main() -> None:
    """Main entry point - execute cloc with passed arguments."""

    cloc_path = get_cloc_path()
    current_platform = platform.system()

    # Verify the binary exists
    if not cloc_path.exists():
        sys.stderr.write(
            f"Error: cloc binary not found at {cloc_path}\n"
            "This may indicate a broken installation.\n"
        )
        sys.exit(1)

    # On Unix-like systems, check if Perl is available
    if current_platform != "Windows" and not check_perl_available():
        sys.stderr.write(
            "Error: Perl is not installed or not in PATH.\n\n"
            "cloc is a Perl script and requires Perl to run on Linux/macOS.\n\n"
            "Install Perl with:\n"
            "  Ubuntu/Debian: sudo apt install perl\n"
            "  CentOS/RHEL:   sudo yum install perl\n"
            "  Arch Linux:    sudo pacman -S perl\n"
            "  macOS:         (usually pre-installed, or brew install perl)\n"
        )
        sys.exit(1)

    args = [str(cloc_path)] + sys.argv[1:]

    result = subprocess.run(
        args,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
