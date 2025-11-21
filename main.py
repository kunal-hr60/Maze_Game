import pygame
import sys
import random

# Game constants
WIDTH, HEIGHT = 900, 700
FPS = 60

#  Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Difficulty 
EASY_LEVELS = [
    (8, 12, 50),   # Level 1
    (10, 15, 45),  # Level 2
    (12, 18, 40),  # Level 3
]

MEDIUM_LEVELS = [
    (15, 20, 35),  # Level 4
    (17, 22, 32),  # Level 5
    (18, 25, 30),  # Level 6
    (20, 28, 28),  # Level 7
]

HARD_LEVELS = [
    (22, 30, 25),  # Level 8
    (25, 35, 22),  # Level 9
    (28, 40, 20),  # Level 10
]

# Game States
MENU = 0
DIFFICULTY_SELECT = 1
PLAYING = 2
LEVEL_COMPLETE = 3
GAME_COMPLETE = 4
PAUSED = 5

#  Maze Generation Class
class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_maze()
        
    def generate_maze(self):
        grid = {(x, y): {'walls': {'N': True, 'S': True, 'E': True, 'W': True}, 'visited': False} 
                for x in range(self.cols) for y in range(self.rows)}
        stack = []
        current = (0, 0)
        grid[current]['visited'] = True
        stack.append(current)

        while stack:
            current = stack.pop()
            x, y = current
            neighbors = []
            
            # Check neighbors
            if y > 0 and not grid[(x, y - 1)]['visited']: neighbors.append((x, y - 1, 'N'))
            if y < self.rows - 1 and not grid[(x, y + 1)]['visited']: neighbors.append((x, y + 1, 'S'))
            if x < self.cols - 1 and not grid[(x + 1, y)]['visited']: neighbors.append((x + 1, y, 'E'))
            if x > 0 and not grid[(x - 1, y)]['visited']: neighbors.append((x - 1, y, 'W'))
            
            if neighbors:
                stack.append(current)
                next_cell_x, next_cell_y, direction = random.choice(neighbors)
                
                # Remove walls
                if direction == 'N': grid[current]['walls']['N'] = False; grid[(next_cell_x, next_cell_y)]['walls']['S'] = False
                elif direction == 'S': grid[current]['walls']['S'] = False; grid[(next_cell_x, next_cell_y)]['walls']['N'] = False
                elif direction == 'E': grid[current]['walls']['E'] = False; grid[(next_cell_x, next_cell_y)]['walls']['W'] = False
                elif direction == 'W': grid[current]['walls']['W'] = False; grid[(next_cell_x, next_cell_y)]['walls']['E'] = False
                
                grid[(next_cell_x, next_cell_y)]['visited'] = True
                stack.append((next_cell_x, next_cell_y))
                
        return grid

# Player Class
class Player:
    def __init__(self):
        self.x, self.y = 0, 0
    
    def draw(self, screen, cell_size):
        rect = pygame.Rect(self.x * cell_size + 2, self.y * cell_size + 2, cell_size - 4, cell_size - 4)
        pygame.draw.rect(screen, RED, rect)

#  Button Class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

#  Drawing Functions 
def draw_maze(screen, maze_grid, rows, cols, cell_size, end_x, end_y):
    for x in range(cols):
        for y in range(rows):
            cell = maze_grid.get((x, y))
            if cell:
                # Draw walls
                if cell['walls']['N']: pygame.draw.line(screen, WHITE, (x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size))
                if cell['walls']['S']: pygame.draw.line(screen, WHITE, (x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))
                if cell['walls']['E']: pygame.draw.line(screen, WHITE, ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))
                if cell['walls']['W']: pygame.draw.line(screen, WHITE, (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size))

    # Draw the end point
    end_rect = pygame.Rect(end_x * cell_size + 2, end_y * cell_size + 2, cell_size - 4, cell_size - 4)
    pygame.draw.rect(screen, GREEN, end_rect)

#  Game Setup Function 
def setup_new_level(difficulty, level_index):
    if difficulty == "easy":
        levels = EASY_LEVELS
    elif difficulty == "medium":
        levels = MEDIUM_LEVELS
    else:  # hard
        levels = HARD_LEVELS
    
    if level_index >= len(levels):
        return None, None, None, None, GAME_COMPLETE

    rows, cols, cell_size = levels[level_index]
    maze = Maze(rows, cols)
    player = Player()
    return maze, player, (rows, cols, cell_size), PLAYING

# Draw Home Screen
def draw_home_screen(screen, buttons, title_font, button_font):
    screen.fill(BLACK)
    
    # Draw title
    title = title_font.render("MAZE RUNNER", True, BLUE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen, button_font)
    
    # Draw instructions
    instructions = [
        "Select difficulty to start playing",
        "Use ARROW KEYS to navigate the maze",
        "Reach the GREEN square to complete each level",
        "Press ESC to pause or return to menu"
    ]
    
    for i, instruction in enumerate(instructions):
        text = pygame.font.SysFont("Arial", 24).render(instruction, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 150 + i * 30))
        screen.blit(text, text_rect)

# Draw Difficulty Selection Screen 
def draw_difficulty_screen(screen, buttons, title_font, button_font):
    screen.fill(BLACK)
    
    # Draw title
    title = title_font.render("SELECT DIFFICULTY", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)
    
    # Draw difficulty descriptions
    difficulties = [
        ("EASY", "3 levels", "Perfect for beginners", GREEN),
        ("MEDIUM", "4 levels", "Moderate challenge", ORANGE),
        ("HARD", "3 levels", "For maze experts", RED)
    ]
    
    for i, (diff, levels, desc, color) in enumerate(difficulties):
        y_pos = HEIGHT // 2 - 80 + i * 120
        
        # Difficulty title
        diff_text = button_font.render(diff, True, color)
        diff_rect = diff_text.get_rect(center=(WIDTH // 2, y_pos))
        screen.blit(diff_text, diff_rect)
        
        # Level info
        level_text = pygame.font.SysFont("Arial", 24).render(levels, True, WHITE)
        level_rect = level_text.get_rect(center=(WIDTH // 2, y_pos + 40))
        screen.blit(level_text, level_rect)
        
        # Description
        desc_text = pygame.font.SysFont("Arial", 20).render(desc, True, GRAY)
        desc_rect = desc_text.get_rect(center=(WIDTH // 2, y_pos + 70))
        screen.blit(desc_text, desc_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen, button_font)

#  Draw Pause Screen 
def draw_pause_screen(screen, buttons, title_font, button_font):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw title
    title = title_font.render("GAME PAUSED", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen, button_font)

#  Draw Level Complete Screen 
def draw_level_complete_screen(screen, level, difficulty, font, title_font):
    screen.fill(BLACK)
    
    title = title_font.render(f"LEVEL {level} COMPLETE!", True, GREEN)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)
    
    diff_text = font.render(f"Difficulty: {difficulty.upper()}", True, WHITE)
    diff_rect = diff_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(diff_text, diff_rect)
    
    if level < get_total_levels(difficulty):
        message = font.render("Press SPACE to continue to next level", True, WHITE)
    else:
        message = font.render("Press SPACE to return to menu", True, WHITE)
        
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(message, message_rect)

#  Draw Game Complete Screen
def draw_game_complete_screen(screen, difficulty, font, title_font):
    screen.fill(BLACK)
    
    title = title_font.render("CONGRATULATIONS!", True, GREEN)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)
    
    message = font.render(f"You completed all {get_total_levels(difficulty)} {difficulty} levels!", True, WHITE)
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(message, message_rect)
    
    continue_text = font.render("Press SPACE to return to menu", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(continue_text, continue_rect)

#  Helper Functions
def get_total_levels(difficulty):
    if difficulty == "easy":
        return len(EASY_LEVELS)
    elif difficulty == "medium":
        return len(MEDIUM_LEVELS)
    else:
        return len(HARD_LEVELS)

def get_level_settings(difficulty, level_index):
    if difficulty == "easy":
        return EASY_LEVELS[level_index]
    elif difficulty == "medium":
        return MEDIUM_LEVELS[level_index]
    else:
        return HARD_LEVELS[level_index]

#  Main Game Loop 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Runner - 10 Levels, 3 Difficulties")
    clock = pygame.time.Clock()
    
    # Fonts
    title_font = pygame.font.SysFont("Arial", 70, bold=True)
    button_font = pygame.font.SysFont("Arial", 40)
    game_font = pygame.font.SysFont("Arial", 30)
    
    # Game state
    game_state = MENU
    current_level = 0
    current_difficulty = "easy"
    
    # Create buttons for home screen
    play_button = Button(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50, "PLAY", BLUE, LIGHT_BLUE)
    exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "EXIT", RED, (200, 0, 0))
    
    # Difficulty selection buttons
    easy_button = Button(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 50, "EASY", GREEN, (100, 255, 100), BLACK)
    medium_button = Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50, "MEDIUM", ORANGE, (255, 200, 100), BLACK)
    hard_button = Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "HARD", RED, (255, 100, 100), BLACK)
    back_button = Button(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50, "BACK", GRAY, LIGHT_BLUE)
    
    # Pause menu buttons
    resume_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "RESUME", GREEN, (100, 255, 100))
    menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "MAIN MENU", BLUE, LIGHT_BLUE)
    
    # Game objects (initialized later)
    maze = None
    player = None
    rows, cols, cell_size = 0, 0, 0
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if game_state == MENU:
                play_button.check_hover(mouse_pos)
                exit_button.check_hover(mouse_pos)
                
                if play_button.is_clicked(mouse_pos, event):
                    game_state = DIFFICULTY_SELECT
                    
                if exit_button.is_clicked(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
                    
            elif game_state == DIFFICULTY_SELECT:
                easy_button.check_hover(mouse_pos)
                medium_button.check_hover(mouse_pos)
                hard_button.check_hover(mouse_pos)
                back_button.check_hover(mouse_pos)
                
                if easy_button.is_clicked(mouse_pos, event):
                    current_difficulty = "easy"
                    current_level = 0
                    maze, player, (rows, cols, cell_size), game_state = setup_new_level(current_difficulty, current_level)
                    
                if medium_button.is_clicked(mouse_pos, event):
                    current_difficulty = "medium"
                    current_level = 0
                    maze, player, (rows, cols, cell_size), game_state = setup_new_level(current_difficulty, current_level)
                    
                if hard_button.is_clicked(mouse_pos, event):
                    current_difficulty = "hard"
                    current_level = 0
                    maze, player, (rows, cols, cell_size), game_state = setup_new_level(current_difficulty, current_level)
                    
                if back_button.is_clicked(mouse_pos, event):
                    game_state = MENU
                    
            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = PAUSED
                    else:
                        old_x, old_y = player.x, player.y
                        
                        # Update player position based on key press and maze walls
                        if 0 <= old_x < cols and 0 <= old_y < rows:
                            current_cell = maze.grid.get((old_x, old_y))
                            if current_cell:
                                if event.key == pygame.K_UP and not current_cell['walls']['N']: player.y -= 1
                                if event.key == pygame.K_DOWN and not current_cell['walls']['S']: player.y += 1
                                if event.key == pygame.K_LEFT and not current_cell['walls']['W']: player.x -= 1
                                if event.key == pygame.K_RIGHT and not current_cell['walls']['E']: player.x += 1

                        # Check for win condition for the current level
                        if player.x == cols - 1 and player.y == rows - 1:
                            current_level += 1
                            if current_level < get_total_levels(current_difficulty):
                                game_state = LEVEL_COMPLETE
                            else:
                                game_state = GAME_COMPLETE
                                
            elif game_state == PAUSED:
                resume_button.check_hover(mouse_pos)
                menu_button.check_hover(mouse_pos)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = PLAYING
                    
                if resume_button.is_clicked(mouse_pos, event):
                    game_state = PLAYING
                    
                if menu_button.is_clicked(mouse_pos, event):
                    game_state = MENU
                            
            elif game_state == LEVEL_COMPLETE or game_state == GAME_COMPLETE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if game_state == LEVEL_COMPLETE:
                        rows, cols, cell_size = get_level_settings(current_difficulty, current_level)
                        maze = Maze(rows, cols)
                        player = Player()
                        game_state = PLAYING
                    else:
                        game_state = MENU
        
        # Drawing
        if game_state == MENU:
            draw_home_screen(screen, [play_button, exit_button], title_font, button_font)
            
        elif game_state == DIFFICULTY_SELECT:
            draw_difficulty_screen(screen, [easy_button, medium_button, hard_button, back_button], title_font, button_font)
            
        elif game_state == PLAYING:
            screen.fill(BLACK)
            draw_maze(screen, maze.grid, rows, cols, cell_size, cols - 1, rows - 1)
            player.draw(screen, cell_size)
            
            # Draw game info
            level_text = game_font.render(f"Level: {current_level + 1}/{get_total_levels(current_difficulty)}", True, WHITE)
            screen.blit(level_text, (10, 10))
            
            diff_text = game_font.render(f"Difficulty: {current_difficulty.upper()}", True, WHITE)
            screen.blit(diff_text, (10, 50))
            
            controls_text = game_font.render("ESC: Pause", True, WHITE)
            screen.blit(controls_text, (WIDTH - 150, 10))
            
        elif game_state == PAUSED:
            # Draw the game in the background
            screen.fill(BLACK)
            draw_maze(screen, maze.grid, rows, cols, cell_size, cols - 1, rows - 1)
            player.draw(screen, cell_size)
            draw_pause_screen(screen, [resume_button, menu_button], title_font, button_font)
            
        elif game_state == LEVEL_COMPLETE:
            draw_level_complete_screen(screen, current_level + 1, current_difficulty, game_font, title_font)
            
        elif game_state == GAME_COMPLETE:
            draw_game_complete_screen(screen, current_difficulty, game_font, title_font)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()