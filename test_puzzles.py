import unittest
from core_puzzles import PathfindingGrid

class TestPuzzles(unittest.TestCase):
    def test_astar_avoids_obstacles(self):
        """Test Case: A* algorithm must find the shortest path around a wall."""
        # Create a 5x5 grid
        grid = PathfindingGrid(5, 5)
        
        # Build a vertical wall in the middle, leaving a gap at the bottom
        grid.toggle_obstacle(2, 0)
        grid.toggle_obstacle(2, 1)
        grid.toggle_obstacle(2, 2)
        grid.toggle_obstacle(2, 3)
        
        start = (0, 0)
        goal = (4, 0)
        
        # Run the generator until completion
        gen = grid.a_star_generator(start, goal)
        final_path = None
        for state in gen:
            if state[3] is not None:
                final_path = state[3]
                
        # Assertions
        self.assertIsNotNone(final_path, "A path should be found")
        self.assertTrue(len(final_path) > 0, "Path should not be empty")
        self.assertEqual(final_path[0], start, "Path must start at origin")
        self.assertEqual(final_path[-1], goal, "Path must end at destination")
        
        # Ensure the path did not cross our wall
        wall_nodes = [(2,0), (2,1), (2,2), (2,3)]
        for node in final_path:
            self.assertNotIn(node, wall_nodes, "Path must not cross obstacles!")

if __name__ == '__main__':
    unittest.main()