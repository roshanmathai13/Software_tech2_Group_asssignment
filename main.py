from phase1_ui import Phase1Screen
from phase2_ui import SortingScreen
from phase2_graphs_ui import GraphScreen
from phase2_heap_ui import HeapScreen
from phase3_puzzles_ui import PathfindingScreen
import pygame
import sys

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
WIDTH, HEIGHT = 800, 600
FPS = 60

# Modern Color Palette
BG_COLOR = (236, 240, 241)         # Light gray background
BTN_COLOR = (41, 128, 185)         # Nice blue
BTN_HOVER_COLOR = (52, 152, 219)   # Lighter blue for hover
TEXT_COLOR = (255, 255, 255)       # White text
TITLE_COLOR = (44, 62, 80)         # Dark gray text

# ==========================================
# UI COMPONENTS (Ensuring Modularity)
# ==========================================
class Button:
    """A reusable button component for intuitive user interaction."""

    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False

    def draw(self, surface):
        # Change color based on hover state (Intuitive Controls)
        color = BTN_HOVER_COLOR if self.is_hovered else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        # Render text centered in the button
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


# ==========================================
# MODULE PLACEHOLDERS (Phase 3)
# ==========================================
# Note: In later steps, these will be moved to separate Python files
# to satisfy the "Clean, modular, well commented code structure" rubric.

def run_placeholder_module(screen, title, font):
    """A temporary screen to demonstrate seamless navigation."""

    clock = pygame.time.Clock()
    back_btn = Button(20, 20, 100, 40, "Back", font)

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.is_clicked(event):
                running = False  # Exit this loop to return to main menu

        # Drawing
        screen.fill(BG_COLOR)

        # Render Title
        title_surf = font.render(
            f"{title} Module (Coming Soon)",
            True,
            TITLE_COLOR
        )

        screen.blit(
            title_surf,
            (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 3)
        )

        # Draw interactive back button
        back_btn.check_hover(mouse_pos)
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DSA Explorer and Visualiser")

    clock = pygame.time.Clock()

    # Fonts
    title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
    btn_font = pygame.font.SysFont("Segoe UI", 24)

    # Setup Main Menu Buttons
    btn_width, btn_height = 250, 50
    start_x = (WIDTH - btn_width) // 2

    buttons = {
        'Data Structures': Button(
            start_x,
            180,
            btn_width,
            btn_height,
            "Phase 1: Data Structures",
            btn_font
        ),

        'Algorithms': Button(
            start_x,
            250,
            btn_width,
            btn_height,
            "Phase 2: Algorithms",
            btn_font
        ),

        'Graphs': Button(
            start_x,
            320,
            btn_width,
            btn_height,
            "Phase 2: Graphs",
            btn_font
        ),

        'Heap': Button(
            start_x,
            390,
            btn_width,
            btn_height,
            "Phase 2: Heap",
            btn_font
        ),

        'Puzzles': Button(
            start_x,
            460,
            btn_width,
            btn_height,
            "Phase 3: Puzzles",
            btn_font
        ),

        'Exit': Button(
            start_x,
            530,
            btn_width,
            btn_height,
            "Exit",
            btn_font
        )
    }

    # Main Event Loop
    running = True

    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Check button clicks
            if buttons['Data Structures'].is_clicked(event):
                # Replace the placeholder with our real screen!
                phase1 = Phase1Screen(screen, btn_font)
                phase1.run()

            elif buttons['Algorithms'].is_clicked(event):
                phase2 = SortingScreen(screen, btn_font)
                phase2.run()

            elif buttons['Graphs'].is_clicked(event):
                phase2_graphs = GraphScreen(screen, btn_font)
                phase2_graphs.run()

            elif buttons['Heap'].is_clicked(event):
                phase2_heap = HeapScreen(screen, btn_font)
                phase2_heap.run()

            elif buttons['Puzzles'].is_clicked(event):
                phase3 = PathfindingScreen(screen, btn_font)
                phase3.run()

            elif buttons['Exit'].is_clicked(event):
                running = False

        # --- Drawing the Main Menu ---
        screen.fill(BG_COLOR)

        # Render Main Title
        title_surf = title_font.render(
            "DSA Explorer",
            True,
            TITLE_COLOR
        )

        screen.blit(
            title_surf,
            (WIDTH // 2 - title_surf.get_width() // 2, 70)
        )

        # Update and draw buttons
        for btn in buttons.values():
            btn.check_hover(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()