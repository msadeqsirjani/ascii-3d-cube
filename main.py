import time
import sys
import os
import math

# Enable Windows ANSI support
if os.name == 'nt':
    os.system('color')
    # Optional: Enable Virtual Terminal processing for better ANSI support
    from ctypes import windll
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.cube import Cube
from src.core.renderer import ASCIIRenderer
from src.utils.screen import clear_terminal
from src.config.settings import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    ROTATION_SPEED, 
    FRAME_DELAY
)

def main():
    # Initialize objects
    cube = Cube()
    renderer = ASCIIRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
    angle_x = 0
    angle_y = 0
    angle_z = 0

    try:
        while True:
            # Clear renderer's screen buffer
            renderer.clear_screen()
            
            # Get rotated vertices
            rotated_vertices = [
                cube.rotate_point(v, angle_x, angle_y, angle_z)
                for v in cube.vertices
            ]
            
            # Project vertices to 2D space
            projected_vertices = [
                renderer.project_point(vertex)
                for vertex in rotated_vertices
            ]
            
            # Draw faces
            for face in cube.faces:
                v1, v2, v3 = face
                # Draw triangle edges
                renderer.draw_line(
                    projected_vertices[v1],
                    projected_vertices[v2]
                )
                renderer.draw_line(
                    projected_vertices[v2],
                    projected_vertices[v3]
                )
                renderer.draw_line(
                    projected_vertices[v3],
                    projected_vertices[v1]
                )
            
            # Clear terminal and display frame
            clear_terminal()
            print(renderer.render_frame())
            
            # Update angles with different speeds for more interesting rotation
            angle_x += ROTATION_SPEED * 0.5
            angle_y += ROTATION_SPEED * 0.7
            angle_z += ROTATION_SPEED * 0.3
            time.sleep(FRAME_DELAY)

    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    finally:
        # Reset colors when exiting
        print('\033[0m')

if __name__ == "__main__":
    main()