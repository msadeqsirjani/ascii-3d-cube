import math

import pytest

from ascii_3d_cube.geometry import Cube


@pytest.fixture
def cube():
    return Cube()


def test_cube_has_expected_mesh(cube):
    assert len(cube.vertices) == 8
    assert len(cube.faces) == 12
    assert all(len(vertex) == 3 for vertex in cube.vertices)
    assert all(len(face) == 3 for face in cube.faces)


@pytest.mark.parametrize(
    ("point", "angles", "expected"),
    [
        ((1, 0, 0), (0, 0, 0), (1, 0, 0)),
        ((0, 1, 0), (math.pi / 2, 0, 0), (0, 0, 1)),
        ((1, 0, 0), (0, math.pi / 2, 0), (0, 0, -1)),
        ((1, 0, 0), (0, 0, math.pi / 2), (0, 1, 0)),
    ],
)
def test_rotate_point(point, angles, expected, cube):
    rotated = cube.rotate_point(point, *angles)
    assert rotated == pytest.approx(expected)


def test_full_rotation_returns_original_point(cube):
    point = (1, 2, 3)
    full_rotation = 2 * math.pi

    rotated = cube.rotate_point(
        point,
        full_rotation,
        full_rotation,
        full_rotation,
    )

    assert rotated == pytest.approx(point)


def test_triangle_mesh_has_cube_edges_and_face_diagonals(cube):
    edges = set()
    for face in cube.faces:
        edges.add(tuple(sorted((face[0], face[1]))))
        edges.add(tuple(sorted((face[1], face[2]))))
        edges.add(tuple(sorted((face[2], face[0]))))

    assert len(edges) == 18
