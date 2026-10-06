"""Small, dependency-free helpers for terminal animation."""

import os
import shutil
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TextIO

ENTER_ALTERNATE_SCREEN = "\033[?1049h\033[2J\033[H\033[?25l\033[40m"
EXIT_ALTERNATE_SCREEN = "\033[0m\033[?25h\033[?1049l"
CURSOR_HOME = "\033[H"


def enable_windows_ansi() -> None:
    """Enable ANSI escape processing in supported Windows terminals."""
    if os.name == "nt":
        os.system("color")


def canvas_size(max_width: int, max_height: int) -> tuple[int, int]:
    """Return a canvas that fits without wrapping or scrolling."""
    terminal = shutil.get_terminal_size((max_width + 1, max_height + 1))
    width = max(1, min(max_width, terminal.columns - 1))
    height = max(1, min(max_height, terminal.lines - 1))
    return width, height


class Terminal:
    """Write flicker-free frames and reliably restore terminal state."""

    def __init__(self, stream: TextIO = sys.stdout) -> None:
        self.stream = stream

    def start(self) -> None:
        self.stream.write(ENTER_ALTERNATE_SCREEN)
        self.stream.flush()

    def display(self, frame: str) -> None:
        self.stream.write(CURSOR_HOME + frame)
        self.stream.flush()

    def stop(self) -> None:
        self.stream.write(EXIT_ALTERNATE_SCREEN)
        self.stream.flush()


@contextmanager
def animation_terminal(stream: TextIO = sys.stdout) -> Iterator[Terminal]:
    """Yield a terminal and restore it even when rendering is interrupted."""
    terminal = Terminal(stream)
    terminal.start()
    try:
        yield terminal
    finally:
        terminal.stop()
