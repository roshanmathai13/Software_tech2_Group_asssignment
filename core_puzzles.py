import heapq

class PathfindingGrid:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.obstacles = set()

    def toggle_obstacle(self, x, y):
        """Adds or removes a wall at the given coordinate."""
        if (x, y) in self.obstacles:
            self.obstacles.remove((x, y))
        else:
            self.obstacles.add((x, y))

    def get_neighbors(self, node):
        """Returns valid adjacent cells (Up, Down, Left, Right)."""
        x, y = node
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            # Check grid boundaries and obstacles
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                if (nx, ny) not in self.obstacles:
                    neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, a, b):
        """Manhattan distance heuristic for A*."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_generator(self, start, goal):
        """
        Yields (closed_set, open_set, current_node, final_path) 
        for Pygame animation.
        """
        # Min-Heap priority queue: stores tuples of (f_score, node)
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        closed_set = set()
        open_set_tracker = {start} # Quick lookup for what is in the heap

        while open_set:
            # Pop the node with the lowest f_score
            current_f, current = heapq.heappop(open_set)
            open_set_tracker.remove(current)
            
            # If we reached the goal, reconstruct the path!
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                yield closed_set, open_set_tracker, current, path
                return

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                    
                # Cost from start to this neighbor
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This path is the best so far, record it!
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    
                    if neighbor not in open_set_tracker:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_tracker.add(neighbor)
                        
            # Yield the current state to Pygame after processing neighbors
            yield closed_set, open_set_tracker, current, None
            
        # If the loop finishes and no path is found
        yield closed_set, open_set_tracker, None, []