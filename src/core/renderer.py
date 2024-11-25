from typing import List, Tuple
import math

class ASCIIRenderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Using block characters and ANSI colors for better visualization
        self.chars = "█▓▒░ "  # More solid block characters
        self.screen = [[' ' for _ in range(width)] for _ in range(height)]
        self.z_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]
        self.colors = [
            '\033[32m',  # Green
            '\033[32;1m',  # Bright Green
            '\033[38;5;34m',  # Custom Green
            '\033[38;5;40m',  # Lighter Green
        ]
        self.reset_color = '\033[0m'

    def clear_screen(self):
        """Clear the screen and z-buffer"""
        self.screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.z_buffer = [[-float('inf') for _ in range(self.width)] for _ in range(self.height)]

    def project_point(self, point: List[float]) -> Tuple[int, int, float]:
        x, y, z = point
        # Improved perspective projection
        scale = 15
        z_offset = 5  # Move cube away from camera
        perspective = scale / (z_offset - z)
        x = int(x * perspective + self.width / 2)
        y = int(y * perspective + self.height / 2)
        return x, y, z

    def get_color_for_depth(self, z: float) -> str:
        """Get color based on depth"""
        z_normalized = (z + 2) / 4  # Normalize z from [-2,2] to [0,1]
        color_index = min(len(self.colors) - 1,
                         max(0, int(z_normalized * len(self.colors))))
        return self.colors[color_index]

    def draw_line(self, start: Tuple[int, int, float], end: Tuple[int, int, float]):
        x1, y1, z1 = start
        x2, y2, z2 = end
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dz = abs(z2 - z1)
        
        x, y = x1, y1
        z = z1
        
        steps = max(dx, dy)
        if steps == 0:
            return
            
        x_inc = (x2 - x1) / steps
        y_inc = (y2 - y1) / steps
        z_inc = (z2 - z1) / steps
        
        for _ in range(int(steps)):
            if (0 <= int(x) < self.width and 
                0 <= int(y) < self.height and 
                z > self.z_buffer[int(y)][int(x)]):
                
                self.z_buffer[int(y)][int(x)] = z
                z_normalized = (z + 2) / 4  # Normalize z from [-2,2] to [0,1]
                color = self.get_color_for_depth(z)
                char = self.chars[min(len(self.chars)-1,
                                   max(0, int(z_normalized * len(self.chars))))]
                self.screen[int(y)][int(x)] = f"{color}{char}{self.reset_color}"
            
            x += x_inc
            y += y_inc
            z += z_inc

    def render_frame(self) -> str:
        """Convert the screen buffer to a string for display"""
        return '\n'.join(''.join(row) for row in self.screen)