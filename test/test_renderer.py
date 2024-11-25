import pytest
from src.core.renderer import ASCIIRenderer

class TestASCIIRenderer:
    @pytest.fixture
    def renderer(self):
        return ASCIIRenderer(width=10, height=5)

    def test_initialization(self, renderer):
        """Test if renderer is properly initialized"""
        assert renderer.width == 10
        assert renderer.height == 5
        assert len(renderer.screen) == 5
        assert len(renderer.screen[0]) == 10
        assert len(renderer.z_buffer) == 5
        assert len(renderer.z_buffer[0]) == 10
        assert renderer.chars == ' .,:-=+*#@'

    def test_clear_screen(self, renderer):
        """Test screen clearing functionality"""
        # Modify screen and z_buffer
        renderer.screen[0][0] = '@'
        renderer.z_buffer[0][0] = 1.0
        
        renderer.clear_screen()
        
        # Verify everything is cleared
        assert all(cell == ' ' for row in renderer.screen for cell in row)
        assert all(cell == float('-inf') for row in renderer.z_buffer for cell in row)

    @pytest.mark.parametrize("point, expected_x, expected_y", [
        ([0, 0, 0], 5, 2),  # Center point
        ([1, 1, 0], 7, 3),  # Positive coordinates
        ([-1, -1, 0], 2, 1),  # Negative coordinates
    ])
    def test_project_point(self, renderer, point, expected_x, expected_y):
        """Test point projection with various inputs"""
        x, y, z = renderer.project_point(point)
        assert x == expected_x
        assert y == expected_y
        assert z == point[2]

    @pytest.mark.parametrize("z_value, expected_char_index", [
        (-2.0, 0),  # Should get first char (space)
        (0.0, len(' .,:-=+*#@')//2),  # Should get middle char
        (2.0, len(' .,:-=+*#@')-1),  # Should get last char (@)
    ])
    def test_get_char_for_depth(self, renderer, z_value, expected_char_index):
        """Test character selection based on depth"""
        char = renderer.get_char_for_depth(z_value)
        assert char == renderer.chars[expected_char_index]

    def test_draw_line_horizontal(self, renderer):
        """Test drawing a horizontal line"""
        start = (1, 2, 0)
        end = (4, 2, 0)
        renderer.draw_line(start, end)
        
        # Check if line is drawn
        assert any(renderer.screen[2][i] != ' ' for i in range(1, 5))

    def test_draw_line_vertical(self, renderer):
        """Test drawing a vertical line"""
        start = (2, 1, 0)
        end = (2, 3, 0)
        renderer.draw_line(start, end)
        
        # Check if line is drawn
        assert any(renderer.screen[i][2] != ' ' for i in range(1, 4))

    def test_draw_line_depth_ordering(self, renderer):
        """Test that closer points override farther points"""
        # Draw far point
        renderer.draw_line((2, 2, -1), (2, 2, -1))
        far_char = renderer.screen[2][2]
        
        # Draw near point
        renderer.draw_line((2, 2, 1), (2, 2, 1))
        near_char = renderer.screen[2][2]
        
        # Near point should have a "heavier" character
        assert renderer.chars.index(near_char) > renderer.chars.index(far_char)

    def test_render_frame(self, renderer):
        """Test frame rendering to string"""
        # Draw something
        renderer.draw_line((1, 1, 0), (3, 3, 0))
        
        frame = renderer.render_frame()
        
        # Verify frame format
        assert isinstance(frame, str)
        lines = frame.split('\n')
        assert len(lines) == renderer.height
        assert all(len(line) == renderer.width for line in lines)