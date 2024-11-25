import math
from typing import List, Tuple

class Cube:
    def __init__(self):
        # Define cube faces instead of just edges
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        
        # Define faces as triangles for better rendering
        self.faces = [
            # Front face
            (0, 1, 2), (0, 2, 3),
            # Back face
            (4, 6, 5), (4, 7, 6),
            # Right face
            (1, 5, 6), (1, 6, 2),
            # Left face
            (4, 0, 3), (4, 3, 7),
            # Top face
            (3, 2, 6), (3, 6, 7),
            # Bottom face
            (4, 5, 1), (4, 1, 0)
        ]

    def rotate_point(self, point: List[float], angle_x: float, angle_y: float, angle_z: float) -> List[float]:
        x, y, z = point
        
        # Rotate around X axis
        y2 = y * math.cos(angle_x) - z * math.sin(angle_x)
        z2 = y * math.sin(angle_x) + z * math.cos(angle_x)
        y, z = y2, z2
        
        # Rotate around Y axis
        x2 = x * math.cos(angle_y) + z * math.sin(angle_y)
        z2 = -x * math.sin(angle_y) + z * math.cos(angle_y)
        x, z = x2, z2
        
        # Rotate around Z axis
        x2 = x * math.cos(angle_z) - y * math.sin(angle_z)
        y2 = x * math.sin(angle_z) + y * math.cos(angle_z)
        x, y = x2, y2
        
        return [x, y, z]