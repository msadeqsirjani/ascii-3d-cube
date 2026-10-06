"""Command-line interface for ASCII 3D Cube."""

import argparse
from collections.abc import Sequence
from typing import Optional

from . import __version__
from .app import run
from .config import AnimationConfig
from .terminal import enable_windows_ansi


def positive_float(value: str) -> float:
    """Parse a strictly positive floating-point argument."""
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def positive_int(value: str) -> int:
    """Parse a strictly positive integer argument."""
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="ascii-cube",
        description="Render a rotating, depth-shaded ASCII cube.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--width", type=positive_int, default=80)
    parser.add_argument("--height", type=positive_int, default=30)
    parser.add_argument("--fps", type=positive_float, default=30.0)
    parser.add_argument("--speed", type=positive_float, default=0.05)
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI colour while retaining ASCII shading",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Parse command-line arguments and start the animation."""
    args = build_parser().parse_args(argv)
    enable_windows_ansi()
    run(
        AnimationConfig(
            max_width=args.width,
            max_height=args.height,
            frames_per_second=args.fps,
            rotation_speed=args.speed,
            use_color=not args.no_color,
        )
    )
