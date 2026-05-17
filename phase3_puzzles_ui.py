import pygame
import sys
from core_puzzles import PathfindingGrid

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
COLS, ROWS = 30, 25  # Grid fits in the right side of the screen
CELL_SIZE = 20

# Colors
BG_COLOR = (236, 240, 241)
GRID_LINE = (200, 200, 200)
WALL_COLOR = (44, 62, 80)
START_COLOR = (46, 204, 113)  # Green
GOAL_COLOR = (231, 76, 60)   # Red
OPEN_COLOR = (174, 214, 241)  # Light Blue
CLOSED_COLOR = (215, 189, 226) # Light Purple
PATH_COLOR = (241, 196, 15)   # Gold
UI_BG = (52, 73, 94)

class PathfindingScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.grid_logic = PathfindingGrid(COLS, ROWS)
        
        # Initial Positions
        self.start_pos = (2, 12)
        self.goal_pos = (27, 12)
        
        # Animation State
        self.anim_gen = None
        self.closed_set = set()
        self.open_set = set()
        self.current_node = None
        self.final_path = None
        self.is_animating = False

    def draw_grid(self):
        offset_x, offset_y = 180, 50 # Push grid away from sidebar
        
        for x in range(COLS):
            for y in range(ROWS):
                rect = pygame.Rect(offset_x + x*CELL_SIZE, offset_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Determine Color
                color = (255, 255, 255) # Default
                if (x, y) in self.grid_logic.obstacles: color = WALL_COLOR
                elif (x, y) == self.start_pos: color = START_COLOR
                elif (x, y) == self.goal_pos: color = GOAL_COLOR
                elif self.final_path and (x, y) in self.final_path: color = PATH_COLOR
                elif (x, y) == self.current_node: color = (255, 255, 0)
                elif (x, y) in self.open_set: color = OPEN_COLOR
                elif (x, y) in self.closed_set: color = CLOSED_COLOR
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_LINE, rect, 1) # Border

    def draw_ui(self):
        pygame.draw.rect(self.screen, UI_BG, (0, 0, 160, HEIGHT))
        title = pygame.font.SysFont(None, 28).render("A* Puzzle", True, (255,255,255))
        self.screen.blit(title, (20, 20))
        
        instructions = [
            "Left-Click: Draw Wall",
            "Right-Click: Move Goal",
            "[SPACE]: Start A*",
            "[R]: Reset Walls",
            "[ESC]: Menu"
        ]
        for i, text in enumerate(instructions):
            inst = pygame.font.SysFont(None, 18).render(text, True, (200,200,200))
            self.screen.blit(inst, (10, 100 + (i * 40)))

    def get_grid_pos(self, mouse_pos):
        x, y = mouse_pos
        grid_x = (x - 180) // CELL_SIZE
        grid_y = (y - 50) // CELL_SIZE
        if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
            return (grid_x, grid_y)
        return None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(BG_COLOR)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: running = False
                    if event.key == pygame.K_r:
                        self.grid_logic.obstacles.clear()
                        self.final_path = None
                    if event.key == pygame.K_SPACE and not self.is_animating:
                        self.final_path = None
                        self.anim_gen = self.grid_logic.a_star_generator(self.start_pos, self.goal_pos)
                        self.is_animating = True

                # Interactive Drawing (Mouse Dragging)
                if pygame.mouse.get_pressed()[0]: # Left Click
                    pos = self.get_grid_pos(pygame.mouse.get_pos())
                    if pos and pos != self.start_pos and pos != self.goal_pos:
                        self.grid_logic.obstacles.add(pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right Click
                    pos = self.get_grid_pos(event.pos)
                    if pos and pos != self.start_pos:
                        self.goal_pos = pos

            # Animation Step
            if self.is_animating:
                try:
                    self.closed_set, self.open_set, self.current_node, self.final_path = next(self.anim_gen)
                except StopIteration:
                    self.is_animating = False

            self.draw_ui()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(60)