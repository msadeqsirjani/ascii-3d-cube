from ascii_3d_cube.app import INITIAL_ANGLES, render_cube
from ascii_3d_cube.geometry import Cube
from ascii_3d_cube.lighting import face_brightness
from ascii_3d_cube.renderer import ASCIIRenderer


def test_render_cube_produces_visible_surface():
    renderer = ASCIIRenderer(60, 24, projection_scale=36)
    frame = render_cube(Cube(), renderer, INITIAL_ANGLES)

    assert len(frame.splitlines()) == 24
    assert any(character != " " for character in frame if character != "\n")


def test_face_brightness_is_normalized():
    brightness = face_brightness(
        (-1.0, -1.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0, -1.0, 1.0),
    )

    assert 0.0 <= brightness <= 1.0
