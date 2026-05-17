import pygame
import sys
from core_algo import (
    generate_random_array, 
    bubble_sort_generator, 
    selection_sort_generator,
    merge_sort_wrapper
)

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (236, 240, 241)
BAR_COLOR = (52, 152, 219)        # Blue for normal bars
HIGHLIGHT_COLOR = (231, 76, 60)   # Red for active comparison/swapping
UI_BG = (44, 62, 80)

class SortingScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.array = generate_random_array(30, 20, 400)
        
        # State tracking
        self.sorting_generator = None
        self.active_indices = []
        self.is_sorting = False
        self.algorithm_name = "None"

    def draw_bars(self):
        """Draws the array as vertical bars."""
        bar_width = (WIDTH - 200) // len(self.array)
        start_x = 200 # Start drawing after the sidebar
        
        for i, val in enumerate(self.array):
            x = start_x + (i * bar_width)
            y = HEIGHT - val
            
            # Rubric Requirement: Highlight compared elements!
            color = HIGHLIGHT_COLOR if i in self.active_indices else BAR_COLOR
            
            rect = pygame.Rect(x, y, bar_width - 2, val)
            pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def draw_ui(self):
        """Draws the sidebar controls."""
        pygame.draw.rect(self.screen, UI_BG, (0, 0, 200, HEIGHT))
        
        title = self.font.render("Sorting", True, (255,255,255))
        self.screen.blit(title, (20, 20))
        
        algo_text = pygame.font.SysFont(None, 24).render(f"Active: {self.algorithm_name}", True, (46, 204, 113))
        self.screen.blit(algo_text, (20, 60))
        
        instructions = [
            "Controls:",
            "[R] Randomize Array",
            "[B] Bubble Sort",
            "[S] Selection Sort",
            "[M] Merge Sort",
            "[SPACE] Pause/Resume",
            "[ESC] Main Menu"
        ]
        
        for i, text in enumerate(instructions):
            inst_surf = pygame.font.SysFont(None, 22).render(text, True, (200,200,200))
            self.screen.blit(inst_surf, (10, 150 + (i * 30)))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(BG_COLOR)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_r:
                        self.array = generate_random_array(30, 20, 400)
                        self.is_sorting = False
                        self.active_indices = []
                        self.algorithm_name = "None"
                        
                    elif event.key == pygame.K_b:
                        self.sorting_generator = bubble_sort_generator(self.array)
                        self.is_sorting = True
                        self.algorithm_name = "Bubble Sort"
                        
                    elif event.key == pygame.K_s:
                        self.sorting_generator = selection_sort_generator(self.array)
                        self.is_sorting = True
                        self.algorithm_name = "Selection Sort"

                    elif event.key == pygame.K_m:
                        self.sorting_generator = merge_sort_wrapper(self.array)
                        self.is_sorting = True
                        self.algorithm_name = "Merge Sort"
                        
                    elif event.key == pygame.K_SPACE:
                        self.is_sorting = not self.is_sorting

            # --- ANIMATION LOGIC ---
            if self.is_sorting and self.sorting_generator:
                try:
                    # Get the next frame of the animation
                    self.array, self.active_indices = next(self.sorting_generator)
                except StopIteration:
                    # The sorting is completely finished
                    self.is_sorting = False
                    self.active_indices = []

            self.draw_ui()
            self.draw_bars()
            
            pygame.display.flip()
            # 30 FPS gives a nice smooth animation speed for sorting
            clock.tick(30)