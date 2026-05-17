import unittest
from core_heap import MaxHeap

class TestMaxHeap(unittest.TestCase):
    def test_heap_insert_and_extract(self):
        """Test Case: Insert values, then extract max. Expected: Extracted in descending order."""
        h = MaxHeap()
        
        # Run generators to completion for testing purposes
        list(h.insert_generator(10))
        list(h.insert_generator(50))
        list(h.insert_generator(30))
        list(h.insert_generator(40))
        
        # The max element should now be at the root (index 0)
        self.assertEqual(h.get_elements()[0], 50, "Max element should be at the root")
        
        # Extract max
        list(h.extract_generator())
        # Next max should be 40
        self.assertEqual(h.get_elements()[0], 40, "New max should bubble to the root")

if __name__ == '__main__':
    unittest.main()