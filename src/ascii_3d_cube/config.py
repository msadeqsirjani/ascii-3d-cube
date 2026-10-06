"""Application configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AnimationConfig:
    """Settings used to render and animate the cube."""

    max_width: int = 80
    max_height: int = 30
    frames_per_second: float = 30.0
    rotation_speed: float = 0.05
    projection_scale: float = 45.0
    character_aspect: float = 2.0
    use_color: bool = True

    @property
    def frame_delay(self) -> float:
        """Return the delay between frames in seconds."""
        return 1.0 / self.frames_per_second
