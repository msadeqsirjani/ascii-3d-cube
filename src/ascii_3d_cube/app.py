"""Animation orchestration."""

import time

from .config import AnimationConfig
from .geometry import Cube
from .lighting import face_brightness
from .renderer import ASCIIRenderer
from .terminal import animation_terminal, canvas_size

INITIAL_ANGLES = (0.45, 0.65, 0.20)
ROTATION_RATIOS = (0.5, 0.7, 0.3)


def create_renderer(config: AnimationConfig) -> ASCIIRenderer:
    """Create a renderer sized for the current terminal."""
    width, height = canvas_size(config.max_width, config.max_height)
    scale = min(config.projection_scale, height * 2.0, width / 1.6)
    return ASCIIRenderer(
        width,
        height,
        projection_scale=scale,
        character_aspect=config.character_aspect,
        use_color=config.use_color,
    )


def render_cube(
    cube: Cube,
    renderer: ASCIIRenderer,
    angles: tuple[float, float, float],
) -> str:
    """Render one cube frame at the supplied Euler angles."""
    renderer.clear()
    rotated = [cube.rotate_point(vertex, *angles) for vertex in cube.vertices]
    projected = [renderer.project(vertex) for vertex in rotated]

    for first, second, third in cube.faces:
        brightness = face_brightness(
            rotated[first],
            rotated[second],
            rotated[third],
        )
        renderer.draw_triangle(
            projected[first],
            projected[second],
            projected[third],
            brightness,
        )

    return renderer.render()


def run(config: AnimationConfig) -> None:
    """Run the animation until the user presses Ctrl+C."""
    cube = Cube()
    renderer = create_renderer(config)
    angles = INITIAL_ANGLES

    try:
        with animation_terminal() as terminal:
            while True:
                terminal.display(render_cube(cube, renderer, angles))
                angles = tuple(
                    angle + config.rotation_speed * ratio
                    for angle, ratio in zip(angles, ROTATION_RATIOS)
                )
                time.sleep(config.frame_delay)
    except KeyboardInterrupt:
        pass
