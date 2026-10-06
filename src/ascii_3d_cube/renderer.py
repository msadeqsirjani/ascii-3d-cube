"""Z-buffered ASCII triangle rasterizer."""

from typing import Optional

from .geometry import Point3D

ProjectedPoint = tuple[int, int, float]

DEFAULT_CHARACTERS = " .,:-=+*#@"
GREEN_PALETTE = (
    "\033[38;5;22m",
    "\033[38;5;28m",
    "\033[38;5;34m",
    "\033[38;5;40m",
    "\033[38;5;46m",
)
RESET_COLOR = "\033[0m"


class ASCIIRenderer:
    """Rasterize projected triangles into a terminal character buffer."""

    def __init__(
        self,
        width: int,
        height: int,
        *,
        projection_scale: float = 12.0,
        character_aspect: float = 2.0,
        camera_distance: float = 10.0,
        use_color: bool = False,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")
        if projection_scale <= 0 or character_aspect <= 0:
            raise ValueError("projection settings must be greater than zero")
        if camera_distance <= 2.0:
            raise ValueError("camera_distance must be greater than 2")

        self.width = width
        self.height = height
        self.projection_scale = projection_scale
        self.character_aspect = character_aspect
        self.camera_distance = camera_distance
        self.use_color = use_color
        self.characters = DEFAULT_CHARACTERS
        self.colors = GREEN_PALETTE
        self.clear()

    def clear(self) -> None:
        """Reset the character, colour, and depth buffers."""
        self.screen = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.color_buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.z_buffer = [
            [-float("inf") for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def project(self, point: Point3D) -> ProjectedPoint:
        """Perspective-project a 3-D point into terminal-cell coordinates."""
        x, y, z = point
        perspective = self.projection_scale / (self.camera_distance - z)
        screen_x = int(
            x * perspective * self.character_aspect + self.width / 2
        )
        screen_y = int(y * perspective + self.height / 2)
        return screen_x, screen_y, z

    @staticmethod
    def _normalized_depth(z: float) -> float:
        return max(0.0, min(1.0, (z + 2.0) / 4.0))

    @staticmethod
    def _palette_index(level: float, palette_size: int) -> int:
        return min(palette_size - 1, int(level * palette_size))

    def character_for_depth(self, z: float) -> str:
        """Return a denser character for geometry nearer the camera."""
        index = self._palette_index(
            self._normalized_depth(z),
            len(self.characters),
        )
        return self.characters[index]

    def color_for_depth(self, z: float) -> str:
        """Return a brighter green for geometry nearer the camera."""
        index = self._palette_index(self._normalized_depth(z), len(self.colors))
        return self.colors[index]

    def _shade_level(self, z: float, brightness: Optional[float]) -> float:
        if brightness is None:
            return self._normalized_depth(z)
        return max(
            0.0,
            min(1.0, brightness * 0.82 + self._normalized_depth(z) * 0.18),
        )

    def _plot(
        self,
        x: int,
        y: int,
        z: float,
        brightness: Optional[float] = None,
    ) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        if z <= self.z_buffer[y][x]:
            return

        shade = self._shade_level(z, brightness)
        self.z_buffer[y][x] = z
        self.screen[y][x] = self.characters[
            self._palette_index(shade, len(self.characters))
        ]
        self.color_buffer[y][x] = self._palette_index(shade, len(self.colors))

    def draw_line(
        self,
        start: ProjectedPoint,
        end: ProjectedPoint,
        brightness: Optional[float] = None,
    ) -> None:
        """Draw a depth-interpolated line, including both endpoints."""
        x1, y1, z1 = start
        x2, y2, z2 = end
        steps = max(abs(x2 - x1), abs(y2 - y1))

        if steps == 0:
            self._plot(x1, y1, z1, brightness)
            return

        for step in range(steps + 1):
            amount = step / steps
            x = round(x1 + (x2 - x1) * amount)
            y = round(y1 + (y2 - y1) * amount)
            z = z1 + (z2 - z1) * amount
            self._plot(x, y, z, brightness)

    def draw_triangle(
        self,
        first: ProjectedPoint,
        second: ProjectedPoint,
        third: ProjectedPoint,
        brightness: Optional[float] = None,
    ) -> None:
        """Fill a projected triangle using barycentric interpolation."""
        x1, y1, z1 = first
        x2, y2, z2 = second
        x3, y3, z3 = third
        denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)

        if denominator == 0:
            self.draw_line(first, second, brightness)
            self.draw_line(second, third, brightness)
            self.draw_line(third, first, brightness)
            return

        min_x = max(0, min(x1, x2, x3))
        max_x = min(self.width - 1, max(x1, x2, x3))
        min_y = max(0, min(y1, y2, y3))
        max_y = min(self.height - 1, max(y1, y2, y3))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                a, b, c = self._barycentric_weights(
                    x + 0.5,
                    y + 0.5,
                    first,
                    second,
                    third,
                    denominator,
                )
                if a < -1e-9 or b < -1e-9 or c < -1e-9:
                    continue

                inverse_depth = (
                    a / (self.camera_distance - z1)
                    + b / (self.camera_distance - z2)
                    + c / (self.camera_distance - z3)
                )
                z = self.camera_distance - 1.0 / inverse_depth
                self._plot(x, y, z, brightness)

    @staticmethod
    def _barycentric_weights(
        x: float,
        y: float,
        first: ProjectedPoint,
        second: ProjectedPoint,
        third: ProjectedPoint,
        denominator: float,
    ) -> tuple[float, float, float]:
        x1, y1, _ = first
        x2, y2, _ = second
        x3, y3, _ = third
        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        return a, b, 1.0 - a - b

    def render(self) -> str:
        """Return the current buffer as a printable frame."""
        if not self.use_color:
            return "\n".join("".join(row) for row in self.screen)
        return "\n".join(
            self._render_color_row(characters, colors)
            for characters, colors in zip(self.screen, self.color_buffer)
        )

    def _render_color_row(
        self,
        characters: list[str],
        color_indexes: list[int],
    ) -> str:
        pieces = []
        active_color = None
        for character, color_index in zip(characters, color_indexes):
            if character == " ":
                if active_color is not None:
                    pieces.append(RESET_COLOR)
                    active_color = None
                pieces.append(character)
                continue

            color = self.colors[color_index]
            if color != active_color:
                pieces.append(color)
                active_color = color
            pieces.append(character)

        if active_color is not None:
            pieces.append(RESET_COLOR)
        return "".join(pieces)
