class Graph:
    def __init__(self):
        self.adj_list = {}
        
    def add_edge(self, u, v):
        """Adds an undirected edge between u and v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def bfs(self, start_node):
        """Standard BFS returning the full path (used for Unit Tests)."""
        visited = []
        queue = [start_node]
        
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.append(curr)
                # Sort neighbors for predictable test results
                for neighbor in sorted(self.adj_list.get(curr, [])):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
        return visited

    def dfs(self, start_node):
        """Standard DFS returning the full path (used for Unit Tests)."""
        visited = []
        stack = [start_node]
        
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.append(curr)
                # Reverse sort so the smallest alphabetical neighbor is popped first
                for neighbor in sorted(self.adj_list.get(curr, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited

    # --- GENERATORS FOR PYGAME ANIMATION ---
    
    def bfs_generator(self, start_node):
        """Yields (visited_list, current_node) for animation."""
        visited = []
        queue = [start_node]
        
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.append(curr)
                yield visited, curr  # Yield state to Pygame
                
                for neighbor in sorted(self.adj_list.get(curr, [])):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
        yield visited, None # Finished

    def dfs_generator(self, start_node):
        """Yields (visited_list, current_node) for animation."""
        visited = []
        stack = [start_node]
        
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.append(curr)
                yield visited, curr  # Yield state to Pygame
                
                for neighbor in sorted(self.adj_list.get(curr, []), reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        yield visited, None # Finished