import pygame
import sys
import math
from core_dsa import Stack, Queue, LinkedList, BST

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (236, 240, 241)
BOX_COLOR = (46, 204, 113)      # Green for data nodes
TEXT_COLOR = (255, 255, 255)
UI_BG = (52, 73, 94)            # Dark sidebar for controls

# Constants for Tree/List Layout
NODE_RADIUS = 20
LEVEL_HEIGHT = 60
HORIZONTAL_GAP = 150

class Phase1Screen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        
        # Initialize all structures
        self.stack = Stack()
        self.queue = Queue()
        self.ll = LinkedList()
        self.bst = BST()
        
        # UI State
        self.input_val = 10 
        self.active_structure = 'Stack' # Default mode

    def draw_arrow(self, start, end):
        """Draws a line with a small arrowhead to represent pointers."""
        pygame.draw.line(self.screen, (52, 73, 94), start, end, 2)
        # Simple arrowhead logic
        angle = math.atan2(start[1] - end[1], start[0] - end[0])
        arrow_len = 10
        p1 = (end[0] + arrow_len * math.cos(angle + math.pi/6), end[1] + arrow_len * math.sin(angle + math.pi/6))
        p2 = (end[0] + arrow_len * math.cos(angle - math.pi/6), end[1] + arrow_len * math.sin(angle - math.pi/6))
        pygame.draw.polygon(self.screen, (52, 73, 94), [end, p1, p2])

    def draw_linked_list(self):
        """Draws nodes in a row with arrows and an interactive hover insertion marker."""
        elements = self.ll.get_elements()
        start_x, start_y = 250, 300
        
        # 1. Draw the Nodes and Arrows
        for i, val in enumerate(elements):
            center = (start_x + i * 80, start_y)
            # Draw Node
            pygame.draw.circle(self.screen, BOX_COLOR, center, NODE_RADIUS)
            text = self.font.render(str(val), True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=center))
            
            # Draw Arrow to next node
            if i < len(elements) - 1:
                next_center = (start_x + (i + 1) * 80 - NODE_RADIUS, start_y)
                self.draw_arrow((center[0] + NODE_RADIUS, center[1]), next_center)

        # 2. Draw Interactive Hover Indicator (Only if in LL mode)
        if self.active_structure == 'LinkedList':
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if mouse is roughly at the same height as the linked list
            if 250 <= mouse_y <= 350:
                # Calculate which position the mouse is hovering over
                relative_x = mouse_x - start_x + 40 # +40 shifts the boundary to the middle of the gaps
                hover_pos = max(0, min(len(elements), relative_x // 80))
                
                # Draw a yellow insertion line
                indicator_x = start_x + (hover_pos * 80) - 40 
                if hover_pos == 0:
                    indicator_x = start_x - 40 # Marker before the head
                    
                pygame.draw.line(self.screen, (241, 196, 15), (indicator_x, start_y - 25), (indicator_x, start_y + 25), 4)
                
                # Draw a small tooltip
                tooltip = pygame.font.SysFont(None, 20).render(f"Insert at pos {hover_pos}", True, (241, 196, 15))
                self.screen.blit(tooltip, (indicator_x - 40, start_y - 45))

    def draw_bst(self, node, x, y, dx):
        """Recursive function to draw BST nodes."""
        if node:
            # Draw lines to children first (so they appear behind nodes)
            if node.left:
                pygame.draw.line(self.screen, (52, 73, 94), (x, y), (x - dx, y + LEVEL_HEIGHT), 2)
                self.draw_bst(node.left, x - dx, y + LEVEL_HEIGHT, dx // 2)
            if node.right:
                pygame.draw.line(self.screen, (52, 73, 94), (x, y), (x + dx, y + LEVEL_HEIGHT), 2)
                self.draw_bst(node.right, x + dx, y + LEVEL_HEIGHT, dx // 2)
            
            # Draw current node
            pygame.draw.circle(self.screen, (52, 152, 219), (x, y), NODE_RADIUS)
            text = self.font.render(str(node.val), True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=(x, y)))

    def draw_stack(self):
        """Draws the stack vertically from bottom to top."""
        elements = self.stack.get_elements()
        start_x, start_y = 450, 500
        box_width, box_height = 100, 40
        
        # Draw container
        pygame.draw.line(self.screen, UI_BG, (start_x - 10, 100), (start_x - 10, start_y + 10), 5)
        pygame.draw.line(self.screen, UI_BG, (start_x + box_width + 10, 100), (start_x + box_width + 10, start_y + 10), 5)
        pygame.draw.line(self.screen, UI_BG, (start_x - 10, start_y + 10), (start_x + box_width + 10, start_y + 10), 5)

        for i, val in enumerate(elements):
            y_pos = start_y - (i * (box_height + 5)) - box_height
            rect = pygame.Rect(start_x, y_pos, box_width, box_height)
            pygame.draw.rect(self.screen, BOX_COLOR, rect, border_radius=5)
            
            text_surf = self.font.render(str(val), True, TEXT_COLOR)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def draw_queue(self):
        """Draws the queue horizontally from left to right."""
        elements = self.queue.get_elements()
        start_x, start_y = 250, 300
        box_width, box_height = 60, 60
        
        # Draw container
        pygame.draw.line(self.screen, UI_BG, (start_x - 10, start_y - 10), (750, start_y - 10), 5)
        pygame.draw.line(self.screen, UI_BG, (start_x - 10, start_y + box_height + 10), (750, start_y + box_height + 10), 5)

        for i, val in enumerate(elements):
            x_pos = start_x + (i * (box_width + 5))
            rect = pygame.Rect(x_pos, start_y, box_width, box_height)
            pygame.draw.rect(self.screen, BOX_COLOR, rect, border_radius=5)
            
            text_surf = self.font.render(str(val), True, TEXT_COLOR)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def draw_ui(self):
        """Draws the control panel."""
        pygame.draw.rect(self.screen, UI_BG, (0, 0, 200, HEIGHT))
        
        # Instructions
        mode_text = self.font.render(f"{self.active_structure}", True, (255,255,255))
        self.screen.blit(mode_text, (20, 20))
        
        inst_text = pygame.font.SysFont(None, 20).render("S: Stack | Q: Queue", True, (200,200,200))
        self.screen.blit(inst_text, (10, 60))

        inst_text_2 = pygame.font.SysFont(None, 20).render("L: LinkedList | B: BST", True, (200,200,200))
        self.screen.blit(inst_text_2, (10, 80))
        
        inst_text3 = pygame.font.SysFont(None, 20).render("Up/Down to change value", True, (200,200,200))
        self.screen.blit(inst_text3, (10, 110))
        
        # Current Value Display
        val_text = self.font.render(f"Value: {self.input_val}", True, (255,255,255))
        self.screen.blit(val_text, (20, 160))
        
        # Action controls
        if self.active_structure == 'LinkedList':
            action_text = pygame.font.SysFont(None, 24).render("CLICK to Insert at Pos", True, BOX_COLOR)
            self.screen.blit(action_text, (20, 220))
        else:
            action_text = pygame.font.SysFont(None, 24).render("SPACE: Insert", True, BOX_COLOR)
            self.screen.blit(action_text, (20, 220))
        
        action_text2 = pygame.font.SysFont(None, 24).render("BACKSPACE: Remove", True, (231, 76, 60)) # Red
        self.screen.blit(action_text2, (20, 260))
        
        action_text3 = pygame.font.SysFont(None, 24).render("ESC: Main Menu", True, (241, 196, 15)) # Yellow
        self.screen.blit(action_text3, (20, HEIGHT - 50))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(BG_COLOR)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # --- MOUSE CLICK LOGIC FOR INSERT_AT_POS ---
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.active_structure == 'LinkedList':
                        mouse_x, mouse_y = event.pos
                        if 250 <= mouse_y <= 350:
                            elements = self.ll.get_elements()
                            relative_x = mouse_x - 250 + 40
                            # Calculate the exact index based on X coordinate
                            clicked_pos = max(0, min(len(elements), relative_x // 80))
                            
                            # Execute the rubric-required insert_at_pos function!
                            self.ll.insert_at_pos(self.input_val, clicked_pos)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Toggle Mode
                    elif event.key == pygame.K_s:
                        self.active_structure = 'Stack'
                    elif event.key == pygame.K_q:
                        self.active_structure = 'Queue'
                    elif event.key == pygame.K_l:
                        self.active_structure = 'LinkedList'
                    elif event.key == pygame.K_b:
                        self.active_structure = 'BST'
                        
                    # Change Value
                    elif event.key == pygame.K_UP:
                        self.input_val += 5
                    elif event.key == pygame.K_DOWN:
                        self.input_val -= 5
                        
                    # Insert / Remove logic for non-mouse structures
                    elif event.key == pygame.K_SPACE:
                        if self.active_structure == 'Stack':
                            self.stack.push(self.input_val)
                        elif self.active_structure == 'Queue':
                            self.queue.enqueue(self.input_val)
                        elif self.active_structure == 'BST':
                            self.bst.insert(self.input_val)
                            
                    elif event.key == pygame.K_BACKSPACE:
                        if self.active_structure == 'Stack':
                            self.stack.pop()
                        elif self.active_structure == 'Queue':
                            self.queue.dequeue()

            self.draw_ui()
            
            # Draw the active structure
            if self.active_structure == 'Stack':
                self.draw_stack()
            elif self.active_structure == 'Queue':
                self.draw_queue()
            elif self.active_structure == 'LinkedList':
                self.draw_linked_list()
            elif self.active_structure == 'BST':
                # Pass the root of the BST and coordinate starting points
                # Starting X is offset by the 200px UI sidebar (middle of remaining 600px -> 500)
                self.draw_bst(self.bst.root, 500, 100, HORIZONTAL_GAP)
                
            pygame.display.flip()
            clock.tick(60)