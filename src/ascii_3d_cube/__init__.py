"""A dependency-free, animated ASCII cube renderer."""

from .config import AnimationConfig
from .geometry import Cube, Point3D
from .renderer import ASCIIRenderer

__all__ = ["ASCIIRenderer", "AnimationConfig", "Cube", "Point3D"]
__version__ = "1.0.0"
