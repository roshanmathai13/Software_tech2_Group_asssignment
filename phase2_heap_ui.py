import pygame
import sys
from core_heap import MaxHeap

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (236, 240, 241)
NODE_COLOR = (52, 152, 219)
HIGHLIGHT_COLOR = (231, 76, 60) # Red for active swapping
TEXT_COLOR = (255, 255, 255)
UI_BG = (44, 62, 80)
NODE_RADIUS = 20

class HeapScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.heap = MaxHeap()
        
        # State
        self.input_val = 50
        self.anim_gen = None
        self.active_indices = []
        self.is_animating = False

    def draw_heap_tree(self):
        """Mathematically draws the array as a complete binary tree."""
        elements = self.heap.get_elements()
        if not elements:
            return
            
        # Helper to get coordinates for a specific index
        def get_pos(idx):
            import math
            if idx == 0: return (450, 100)
            
            level = int(math.log2(idx + 1))
            max_nodes_in_level = 2 ** level
            position_in_level = idx - (max_nodes_in_level - 1)
            
            # Spread nodes out based on what level they are on
            y = 100 + (level * 80)
            width_spread = 400 / (level + 1)
            start_x = 450 - (width_spread * (max_nodes_in_level - 1)) / 2
            x = start_x + (position_in_level * width_spread)
            return (x, y)

        # 1. Draw connecting lines first (so they are under the nodes)
        for i in range(len(elements)):
            parent = (i - 1) // 2
            if i > 0:
                pygame.draw.line(self.screen, UI_BG, get_pos(parent), get_pos(i), 3)

        # 2. Draw nodes
        for i, val in enumerate(elements):
            pos = get_pos(i)
            color = HIGHLIGHT_COLOR if i in self.active_indices else NODE_COLOR
            pygame.draw.circle(self.screen, color, pos, NODE_RADIUS)
            
            text = self.font.render(str(val), True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=pos))

    def draw_ui(self):
        pygame.draw.rect(self.screen, UI_BG, (0, 0, 200, HEIGHT))
        
        title = self.font.render("Max Heap", True, (255,255,255))
        self.screen.blit(title, (20, 20))
        
        val_txt = self.font.render(f"Value: {self.input_val}", True, (241, 196, 15))
        self.screen.blit(val_txt, (20, 80))

        instructions = [
            "[UP/DOWN] Change Value",
            "[SPACE] Insert Value",
            "[BACKSPACE] Extract Max",
            "[ESC] Main Menu"
        ]
        for i, text in enumerate(instructions):
            inst_surf = pygame.font.SysFont(None, 20).render(text, True, (200,200,200))
            self.screen.blit(inst_surf, (10, 150 + (i * 30)))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        ANIM_SPEED = 600 # ms between steps
        last_update = pygame.time.get_ticks()

        while running:
            self.screen.fill(BG_COLOR)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # Only accept input if we aren't currently animating a bubble-up/down!
                if event.type == pygame.KEYDOWN and not self.is_animating:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.input_val += 5
                    elif event.key == pygame.K_DOWN:
                        self.input_val -= 5
                    elif event.key == pygame.K_SPACE:
                        self.anim_gen = self.heap.insert_generator(self.input_val)
                        self.is_animating = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.anim_gen = self.heap.extract_generator()
                        self.is_animating = True

            # --- ANIMATION LOGIC ---
            if self.is_animating and now - last_update > ANIM_SPEED:
                try:
                    # Update the heap array state and get the highlighted indices
                    _, self.active_indices = next(self.anim_gen)
                    last_update = now
                except StopIteration:
                    self.is_animating = False
                    self.active_indices = []

            self.draw_ui()
            self.draw_heap_tree()
            pygame.display.flip()
            clock.tick(60)