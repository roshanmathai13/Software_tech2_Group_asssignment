import pygame
import sys
from core_graph import Graph

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (236, 240, 241)
NODE_COLOR = (52, 152, 219)      # Blue
VISITED_COLOR = (46, 204, 113)   # Green
ACTIVE_COLOR = (241, 196, 15)    # Yellow
TEXT_COLOR = (255, 255, 255)
UI_BG = (44, 62, 80)
NODE_RADIUS = 25

class GraphScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.graph = Graph()
        
        # Setup the graph structure (A-B-C-D-E)
        self.setup_sample_graph()
        
        # Define visual positions for nodes
        self.node_positions = {
            'A': (400, 150),
            'B': (300, 250),
            'C': (500, 250),
            'D': (300, 400),
            'E': (500, 400)
        }
        
        # Animation State
        self.traversal_gen = None
        self.visited_nodes = []
        self.current_node = None
        self.is_animating = False
        self.mode = "BFS" # Default mode

    def setup_sample_graph(self):
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('A', 'C')
        self.graph.add_edge('B', 'D')
        self.graph.add_edge('C', 'E')
        self.graph.add_edge('D', 'E')

    def draw_graph(self):
        # 1. Draw Edges (Lines)
        for u in self.graph.adj_list:
            for v in self.graph.adj_list[u]:
                pygame.draw.line(self.screen, UI_BG, self.node_positions[u], self.node_positions[v], 3)

        # 2. Draw Nodes (Circles)
        for node, pos in self.node_positions.items():
            color = NODE_COLOR
            if node == self.current_node:
                color = ACTIVE_COLOR
            elif node in self.visited_nodes:
                color = VISITED_COLOR
                
            pygame.draw.circle(self.screen, color, pos, NODE_RADIUS)
            # Label
            text = self.font.render(node, True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=pos))

    def draw_ui(self):
        pygame.draw.rect(self.screen, UI_BG, (0, 0, 200, HEIGHT))
        
        title = self.font.render("Graph Search", True, (255,255,255))
        self.screen.blit(title, (20, 20))
        
        mode_txt = pygame.font.SysFont(None, 24).render(f"Mode: {self.mode}", True, (46, 204, 113))
        self.screen.blit(mode_txt, (20, 60))

        instructions = [
            "[T] Toggle BFS/DFS",
            "[Click a Node] to Start",
            "[R] Reset Graph",
            "[ESC] Main Menu"
        ]
        for i, text in enumerate(instructions):
            inst_surf = pygame.font.SysFont(None, 20).render(text, True, (200,200,200))
            self.screen.blit(inst_surf, (10, 150 + (i * 30)))

    def handle_click(self, pos):
        """Checks if a node was clicked and starts traversal."""
        for node, node_pos in self.node_positions.items():
            # Standard circle collision math
            dist = ((pos[0] - node_pos[0])**2 + (pos[1] - node_pos[1])**2)**0.5
            if dist <= NODE_RADIUS:
                # Start new animation
                self.visited_nodes = []
                if self.mode == "BFS":
                    self.traversal_gen = self.graph.bfs_generator(node)
                else:
                    self.traversal_gen = self.graph.dfs_generator(node)
                self.is_animating = True
                break

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        # Timer for animation speed (slow it down so users can see the steps)
        ANIM_SPEED = 800 # milliseconds
        last_update = pygame.time.get_ticks()

        while running:
            self.screen.fill(BG_COLOR)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_t:
                        self.mode = "DFS" if self.mode == "BFS" else "BFS"
                    elif event.key == pygame.K_r:
                        self.visited_nodes = []
                        self.current_node = None
                        self.is_animating = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            # --- ANIMATION LOGIC ---
            if self.is_animating and now - last_update > ANIM_SPEED:
                try:
                    self.visited_nodes, self.current_node = next(self.traversal_gen)
                    last_update = now
                except StopIteration:
                    self.is_animating = False
                    self.current_node = None

            self.draw_ui()
            self.draw_graph()
            pygame.display.flip()
            clock.tick(60)