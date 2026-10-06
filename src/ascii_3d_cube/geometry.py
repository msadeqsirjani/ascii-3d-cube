"""Cube geometry and three-dimensional transformations."""

import math
from collections.abc import Sequence
from dataclasses import dataclass

Point3D = tuple[float, float, float]
Triangle = tuple[int, int, int]


@dataclass(frozen=True)
class Cube:
    """A unit cube represented as a triangle mesh."""

    vertices: tuple[Point3D, ...] = (
        (-1.0, -1.0, -1.0),
        (1.0, -1.0, -1.0),
        (1.0, 1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
        (1.0, -1.0, 1.0),
        (1.0, 1.0, 1.0),
        (-1.0, 1.0, 1.0),
    )
    faces: tuple[Triangle, ...] = (
        (0, 1, 2),
        (0, 2, 3),
        (4, 6, 5),
        (4, 7, 6),
        (1, 5, 6),
        (1, 6, 2),
        (4, 0, 3),
        (4, 3, 7),
        (3, 2, 6),
        (3, 6, 7),
        (4, 5, 1),
        (4, 1, 0),
    )

    @staticmethod
    def rotate_point(
        point: Sequence[float],
        angle_x: float,
        angle_y: float,
        angle_z: float,
    ) -> Point3D:
        """Rotate a point around the X, Y, and Z axes, in that order."""
        x, y, z = point

        cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

        cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
        x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

        cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

        return x, y, z
