class Stack:
    """A standard Last-In-First-Out (LIFO) Stack."""
    
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None  # Prevent crashing if popping an empty stack

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_elements(self):
        """Returns a copy of elements for Pygame visualization."""
        return self.items.copy()


class Queue:
    """A standard First-In-First-Out (FIFO) Queue."""
    
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_elements(self):
        """Returns a copy of elements for Pygame visualization."""
        return self.items.copy()


class Node:
    """A standard node for a Singly Linked List."""
    
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """A Singly Linked List with insertion by position."""
    
    def __init__(self):
        self.head = None

    def append(self, data):
        if not self.head:
            self.head = Node(data)
            return

        curr = self.head
        while curr.next:
            curr = curr.next

        curr.next = Node(data)

    def insert_at_pos(self, data, pos):
        """Inserts a node at a specific zero-indexed position."""
        
        new_node = Node(data)

        if pos == 0:
            new_node.next = self.head
            self.head = new_node
            return

        curr = self.head
        curr_pos = 0

        # Traverse to the node just before the insertion point
        while curr and curr_pos < pos - 1:
            curr = curr.next
            curr_pos += 1

        if curr is None:
            # Position out of bounds, append instead
            self.append(data)
        else:
            new_node.next = curr.next
            curr.next = new_node

    def get_elements(self):
        """Returns list of elements for Pygame visualization."""
        
        elements = []
        curr = self.head

        while curr:
            elements.append(curr.data)
            curr = curr.next

        return elements


class TreeNode:
    """A node for a Binary Search Tree."""
    
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None


class BST:
    """A standard Binary Search Tree."""
    
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert_recursive(node.left, key)

        elif key > node.val:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert_recursive(node.right, key)

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)