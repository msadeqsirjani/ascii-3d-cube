import pytest

from ascii_3d_cube.renderer import DEFAULT_CHARACTERS, ASCIIRenderer


@pytest.fixture
def renderer():
    return ASCIIRenderer(width=10, height=5)


def test_initialization(renderer):
    assert renderer.width == 10
    assert renderer.height == 5
    assert renderer.characters == DEFAULT_CHARACTERS
    assert len(renderer.screen) == 5
    assert len(renderer.screen[0]) == 10


@pytest.mark.parametrize(
    ("point", "expected"),
    [
        ((0, 0, 0), (5, 2, 0)),
        ((1, 1, 0), (7, 3, 0)),
        ((-1, -1, 0), (2, 1, 0)),
    ],
)
def test_project(renderer, point, expected):
    assert renderer.project(point) == expected


@pytest.mark.parametrize(
    ("depth", "character_index"),
    [
        (-2.0, 0),
        (0.0, len(DEFAULT_CHARACTERS) // 2),
        (2.0, len(DEFAULT_CHARACTERS) - 1),
    ],
)
def test_character_for_depth(renderer, depth, character_index):
    assert renderer.character_for_depth(depth) == DEFAULT_CHARACTERS[character_index]


def test_clear_resets_buffers(renderer):
    renderer.draw_line((1, 1, 0), (3, 3, 0))
    renderer.clear()

    assert all(cell == " " for row in renderer.screen for cell in row)
    assert all(depth == float("-inf") for row in renderer.z_buffer for depth in row)


def test_draw_line_includes_single_point(renderer):
    renderer.draw_line((2, 2, 0), (2, 2, 0))
    assert renderer.screen[2][2] != " "


def test_nearer_geometry_wins_depth_test(renderer):
    renderer.draw_line((2, 2, -1), (2, 2, -1))
    far_character = renderer.screen[2][2]
    renderer.draw_line((2, 2, 1), (2, 2, 1))

    assert DEFAULT_CHARACTERS.index(renderer.screen[2][2]) > (
        DEFAULT_CHARACTERS.index(far_character)
    )


def test_draw_triangle_fills_its_interior(renderer):
    renderer.draw_triangle((1, 1, 0), (8, 1, 0), (4, 4, 0))
    assert renderer.screen[2][4] != " "


def test_render_returns_fixed_size_plain_text(renderer):
    renderer.draw_line((1, 1, 0), (3, 3, 0))
    lines = renderer.render().splitlines()

    assert len(lines) == renderer.height
    assert all(len(line) == renderer.width for line in lines)


def test_invalid_dimensions_are_rejected():
    with pytest.raises(ValueError, match="width and height"):
        ASCIIRenderer(0, 10)
