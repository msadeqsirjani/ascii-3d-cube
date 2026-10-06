"""Backward-compatible launcher for running the project from a clone."""

import sys
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).resolve().parent / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from ascii_3d_cube.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
