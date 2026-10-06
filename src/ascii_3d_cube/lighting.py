"""Lighting helpers for the ASCII renderer."""

import math

from .geometry import Point3D

DEFAULT_LIGHT_DIRECTION: Point3D = (-0.35, -0.55, 0.76)


def face_brightness(
    first: Point3D,
    second: Point3D,
    third: Point3D,
    light: Point3D = DEFAULT_LIGHT_DIRECTION,
) -> float:
    """Calculate ambient and diffuse lighting for one triangle."""
    edge_a = tuple(second[index] - first[index] for index in range(3))
    edge_b = tuple(third[index] - first[index] for index in range(3))

    # The mesh uses inward winding, so invert the cross-product normal.
    normal = (
        -(edge_a[1] * edge_b[2] - edge_a[2] * edge_b[1]),
        -(edge_a[2] * edge_b[0] - edge_a[0] * edge_b[2]),
        -(edge_a[0] * edge_b[1] - edge_a[1] * edge_b[0]),
    )
    length = math.sqrt(sum(component * component for component in normal))
    if length == 0:
        return 0.0

    unit_normal = tuple(component / length for component in normal)
    diffuse = max(
        0.0,
        sum(unit_normal[index] * light[index] for index in range(3)),
    )
    return min(1.0, 0.18 + diffuse * 0.82)
