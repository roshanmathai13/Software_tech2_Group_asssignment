import unittest
from core_dsa import Stack, Queue, LinkedList, BST


class TestDataStructures(unittest.TestCase):

    def test_stack_push_pop_sequence(self):
        """Test Case: Push 3 items, pop 2. Expected: Final size = 1, correct order."""
        
        s = Stack()
        
        s.push(10)
        s.push(20)
        s.push(30)

        s.pop()  # Removes 30
        s.pop()  # Removes 20

        self.assertEqual(s.size(), 1, "Stack size should be 1")
        self.assertEqual(s.peek(), 10, "Top element should be 10")

    def test_queue_enqueue_dequeue(self):
        """Test Case: Enqueue 4 items, dequeue 3. Expected: FIFO order maintained."""
        
        q = Queue()

        q.enqueue("A")
        q.enqueue("B")
        q.enqueue("C")
        q.enqueue("D")

        q.dequeue()  # Removes A
        q.dequeue()  # Removes B
        q.dequeue()  # Removes C

        self.assertEqual(q.size(), 1, "Queue size should be 1")
        self.assertEqual(q.get_elements()[0], "D", "Remaining element should be D")

    def test_linked_list_insertion_at_pos(self):
        """
        Test Case: Insert node with value 10 at position 2.
        Expected: Node present in correct location in list.
        """
        
        ll = LinkedList()

        ll.append(5)   # Pos 0
        ll.append(15)  # Pos 1
        ll.append(20)  # Pos 2 (will shift to 3)

        ll.insert_at_pos(10, 2)

        elements = ll.get_elements()

        self.assertEqual(elements[2], 10, "Value at position 2 should be 10")
        self.assertEqual(
            elements,
            [5, 15, 10, 20],
            "List order should be correct"
        )

    def test_bst_insert_and_inorder_traversal(self):
        """
        Test Case: Insert [50, 30, 70]; inorder traversal.
        Expected: Traversal order: 30, 50, 70.
        """
        
        tree = BST()

        tree.insert(50)
        tree.insert(30)
        tree.insert(70)

        traversal = tree.inorder_traversal()

        self.assertEqual(
            traversal,
            [30, 50, 70],
            "Inorder traversal should be sorted"
        )


if __name__ == '__main__':
    unittest.main()