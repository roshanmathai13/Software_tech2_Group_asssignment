import unittest
from core_graph import Graph

class TestGraphTraversals(unittest.TestCase):
    def setUp(self):
        """Builds a sample graph before every test."""
        self.g = Graph()
        # Creating a standard graph: 
        #    A
        #   / \
        #  B   C
        #  |   |
        #  D---E
        self.g.add_edge('A', 'B')
        self.g.add_edge('A', 'C')
        self.g.add_edge('B', 'D')
        self.g.add_edge('C', 'E')
        self.g.add_edge('D', 'E')

    def test_bfs_traversal(self):
        """Test Case: Visit nodes reachable from 'A'. Expected: Correct BFS order."""
        expected_path = ['A', 'B', 'C', 'D', 'E']
        actual_path = self.g.bfs('A')
        self.assertEqual(actual_path, expected_path, "BFS order should match level-by-level traversal")

    def test_dfs_traversal(self):
        """Test Case: DFS order matches expected path starting from 'C'."""
        # Starting from C, neighbors are A and E. 
        # Alphabetical DFS will visit A first -> B -> D -> E
        expected_path = ['C', 'A', 'B', 'D', 'E']
        actual_path = self.g.dfs('C')
        self.assertEqual(actual_path, expected_path, "DFS order should match depth-first logic")

if __name__ == '__main__':
    unittest.main()