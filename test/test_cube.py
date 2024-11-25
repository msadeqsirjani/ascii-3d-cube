import pytest
import math
from src.core.cube import Cube

class TestCube:
    @pytest.fixture
    def cube(self):
        return Cube()

    def test_cube_initialization(self, cube):
        """Test if cube is properly initialized with correct vertices and faces"""
        # Test vertices
        assert len(cube.vertices) == 8  # A cube has 8 vertices
        for vertex in cube.vertices:
            assert len(vertex) == 3  # Each vertex should have x, y, z coordinates
            assert all(isinstance(coord, (int, float)) for coord in vertex)

        # Test faces
        assert len(cube.faces) == 12  # 6 faces * 2 triangles per face
        for face in cube.faces:
            assert len(face) == 3  # Each face should be a triangle (3 vertices)
            assert all(0 <= vertex_idx < 8 for vertex_idx in face)  # Valid vertex indices

    @pytest.mark.parametrize("point, angles, expected", [
        # No rotation
        ([1, 0, 0], (0, 0, 0), [1, 0, 0]),
        # 90° rotation around X axis
        ([0, 1, 0], (math.pi/2, 0, 0), [0, 0, 1]),
        # 90° rotation around Y axis
        ([1, 0, 0], (0, math.pi/2, 0), [0, 0, -1]),
        # 90° rotation around Z axis
        ([1, 0, 0], (0, 0, math.pi/2), [0, 1, 0]),
    ])
    def test_rotate_point(self, cube, point, angles, expected):
        """Test point rotation with various angles"""
        angle_x, angle_y, angle_z = angles
        rotated = cube.rotate_point(point, angle_x, angle_y, angle_z)
        
        # Check if result matches expected with small floating point tolerance
        assert len(rotated) == 3
        for actual, expected_val in zip(rotated, expected):
            assert abs(actual - expected_val) < 1e-10

    def test_rotate_point_360_degrees(self, cube):
        """Test that rotating 360 degrees returns to starting position"""
        original_point = [1, 2, 3]
        full_rotation = 2 * math.pi
        
        rotated = cube.rotate_point(
            original_point, 
            full_rotation, 
            full_rotation, 
            full_rotation
        )
        
        # Check if point returns to original position
        for original, rotated_val in zip(original_point, rotated):
            assert abs(original - rotated_val) < 1e-10

    def test_vertex_connectivity(self, cube):
        """Test if cube faces form a closed surface"""
        # Create a set of all edges
        edges = set()
        for face in cube.faces:
            # Add all three edges of the triangle
            edges.add(tuple(sorted([face[0], face[1]])))
            edges.add(tuple(sorted([face[1], face[2]])))
            edges.add(tuple(sorted([face[2], face[0]])))
        
        # A cube should have 12 unique edges
        assert len(edges) == 12