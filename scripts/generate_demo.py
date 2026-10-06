"""Generate the animated README demo from real renderer frames."""

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from ascii_3d_cube.app import render_cube  # noqa: E402
from ascii_3d_cube.geometry import Cube  # noqa: E402
from ascii_3d_cube.renderer import ASCIIRenderer  # noqa: E402

WIDTH = 80
HEIGHT = 23
CELL_WIDTH = 7.8
CELL_HEIGHT = 14.0
PADDING = 18
FRAME_COUNT = 80
FRAME_DELAY = 4
BACKGROUND = "#030014"
FOREGROUND_COLORS = ("#005f00", "#008700", "#00af00", "#00d700", "#00ff00")


def animation_angles(frame_number: int) -> tuple[float, float, float]:
    """Return a smooth, seamless rotation for one frame."""
    progress = 2.0 * math.pi * frame_number / FRAME_COUNT
    return (
        0.45 + 0.22 * math.sin(progress),
        0.65 + progress,
        0.20 + 0.12 * math.sin(progress * 2.0),
    )


def frame_svg(renderer: ASCIIRenderer) -> str:
    """Convert a rendered character buffer into a terminal-like SVG."""
    pixel_width = int(WIDTH * CELL_WIDTH + PADDING * 2)
    pixel_height = int(HEIGHT * CELL_HEIGHT + PADDING * 2)
    text_elements = []

    for row_index, (characters, color_indexes) in enumerate(
        zip(renderer.screen, renderer.color_buffer)
    ):
        column = 0
        while column < WIDTH:
            if characters[column] == " ":
                column += 1
                continue

            run_start = column
            color_index = color_indexes[column]
            while (
                column < WIDTH
                and characters[column] != " "
                and color_indexes[column] == color_index
            ):
                column += 1

            text = escape("".join(characters[run_start:column]))
            x = PADDING + run_start * CELL_WIDTH
            y = PADDING + (row_index + 0.82) * CELL_HEIGHT
            color = FOREGROUND_COLORS[color_index]
            text_elements.append(
                f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}">{text}</text>'
            )

    body = "\n  ".join(text_elements)
    return f"""<svg xmlns="http://www.w3.org/2000/svg"
  width="{pixel_width}" height="{pixel_height}"
  viewBox="0 0 {pixel_width} {pixel_height}">
  <rect width="100%" height="100%" fill="{BACKGROUND}"/>
  <g font-family="Menlo, Monaco, monospace" font-size="13"
     font-weight="400" xml:space="preserve">
  {body}
  </g>
</svg>
"""


def generate(output: Path) -> None:
    """Render SVG frames and combine them into an optimized GIF."""
    magick = shutil.which("magick")
    if magick is None:
        raise SystemExit("ImageMagick is required: https://imagemagick.org")

    cube = Cube()
    renderer = ASCIIRenderer(
        WIDTH,
        HEIGHT,
        projection_scale=45,
        character_aspect=2.0,
        use_color=True,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ascii-cube-demo-") as directory:
        temporary_directory = Path(directory)
        frames = []
        for frame_number in range(FRAME_COUNT):
            render_cube(cube, renderer, animation_angles(frame_number))
            frame_path = temporary_directory / f"frame-{frame_number:03d}.svg"
            frame_path.write_text(frame_svg(renderer), encoding="utf-8")
            frames.append(str(frame_path))

        command = [
            magick,
            "-background",
            BACKGROUND,
            "-delay",
            str(FRAME_DELAY),
            "-loop",
            "0",
            *frames,
            "-layers",
            "Optimize",
            str(output),
        ]
        subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "docs/images/cube_demo.gif",
    )
    args = parser.parse_args()
    generate(args.output)
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
