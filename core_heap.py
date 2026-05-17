class MaxHeap:
    def __init__(self):
        self.heap = []

    def get_elements(self):
        return self.heap.copy()

    def insert_generator(self, val):
        """Yields (array_state, active_indices) while bubbling up."""
        self.heap.append(val)
        idx = len(self.heap) - 1
        yield self.heap, [idx]  # Show the newly added node at the bottom
        
        while idx > 0:
            parent_idx = (idx - 1) // 2
            yield self.heap, [idx, parent_idx] # Highlight the nodes being compared
            
            if self.heap[idx] > self.heap[parent_idx]:
                # Swap if child is greater than parent
                self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
                idx = parent_idx
                yield self.heap, [idx] # Show the node in its new position
            else:
                break # It's in the right spot!
                
        yield self.heap, [] # Finished

    def extract_generator(self):
        """Yields (array_state, active_indices) while bubbling down."""
        if len(self.heap) == 0:
            yield self.heap, []
            return
            
        if len(self.heap) == 1:
            self.heap.pop()
            yield self.heap, []
            return
            
        # 1. Swap root with the very last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        yield self.heap, [0, len(self.heap)-1]
        
        # 2. Remove the old root (which is now at the end)
        self.heap.pop()
        yield self.heap, [0]
        
        # 3. Bubble Down
        idx = 0
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            
            if left < len(self.heap) and self.heap[left] > self.heap[largest]:
                largest = left
            if right < len(self.heap) and self.heap[right] > self.heap[largest]:
                largest = right
                
            if largest != idx:
                yield self.heap, [idx, largest] # Highlight comparison
                # Swap
                self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
                idx = largest
                yield self.heap, [idx] # Highlight new position
            else:
                break
                
        yield self.heap, [] # Finished