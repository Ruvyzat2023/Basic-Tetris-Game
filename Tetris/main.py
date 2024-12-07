import pygame
import random
from music import BackgroundMusic  # Import the BackgroundMusic class

# Initialize pygame
pygame.init()

# Define the screen size (450x600)
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = 10  # Number of columns for the playing area
ROWS = SCREEN_HEIGHT // BLOCK_SIZE  # Number of rows based on the height

# Define colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# Define tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]  # J
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

# Tetromino class
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLUMNS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def draw(self, screen):
        for row_idx, row in enumerate(self.shape):
            for col_idx, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, self.color,
                                     pygame.Rect((self.x + col_idx) * BLOCK_SIZE,
                                                 (self.y + row_idx) * BLOCK_SIZE,
                                                 BLOCK_SIZE, BLOCK_SIZE))

# Function to draw the ghost piece
def draw_ghost_piece(screen, piece, grid):
    # Create a copy of the piece
    ghost_piece = Tetromino(piece.shape, WHITE)  # Use white for the ghost piece
    ghost_piece.x = piece.x
    ghost_piece.y = piece.y

    # Simulate the fall of the ghost piece
    while valid_space(ghost_piece, grid):
        ghost_piece.y += 1
    ghost_piece.y -= 1  # Move back to the last valid position

    # Draw the ghost piece (fully filled in white)
    for row_idx, row in enumerate(ghost_piece.shape):
        for col_idx, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, WHITE, pygame.Rect(
                    (ghost_piece.x + col_idx) * BLOCK_SIZE,
                    (ghost_piece.y + row_idx) * BLOCK_SIZE,
                    BLOCK_SIZE, BLOCK_SIZE))  # Fully filled

# Function to create the grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

# Check if a space is valid for placing a piece
def valid_space(piece, grid):
    for row_idx, row in enumerate(piece.shape):
        for col_idx, val in enumerate(row):
            if val:
                x = piece.x + col_idx
                y = piece.y + row_idx
                if x < 0 or x >= COLUMNS or y >= ROWS:
                    return False
                if y >= 0 and grid[y][x] != BLACK:
                    return False
    return True

# Function to clear full rows
def clear_rows(grid, locked_positions, level):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        if BLACK not in grid[i]:
            increment += 1
            index = i
            for j in range(len(grid[i])):
                try:
                    del locked_positions[(j, i)]
                except ValueError:
                    continue
    if increment > 0:
        # Shift down all rows above the cleared row
        for key in list(locked_positions):
            x, y = key
            if y < index:
                new_key = (x, y + increment)
                locked_positions[new_key] = locked_positions.pop(key)
    return increment

# Function to draw the grid
def draw_grid(screen, grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(screen, grid[i][j], pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for i in range(ROWS):
        pygame.draw.line(screen, WHITE, (0, i * BLOCK_SIZE), (COLUMNS * BLOCK_SIZE, i * BLOCK_SIZE))  # horizontal lines
    for j in range(COLUMNS):
        pygame.draw.line(screen, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, ROWS * BLOCK_SIZE))  # vertical lines
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, COLUMNS * BLOCK_SIZE, ROWS * BLOCK_SIZE), 5)

# Function to calculate score
def calculate_score(cleared_rows, level):
    return cleared_rows * level * 100

# Function to draw the score
def draw_score(screen, score, lines_cleared, level):
    font = pygame.font.SysFont('arial', 30)
    label = font.render(f"Score: {score}", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH - label.get_width() - 20, 20))
    label = font.render(f"Lines: {lines_cleared}", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH - label.get_width() - 20, 60))
    label = font.render(f"Level: {level}", True, WHITE)
    screen.blit(label, (SCREEN_WIDTH - label.get_width() - 20, 100))

def main():
    # Initialize screen and other game elements
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    grid = create_grid()
    locked_positions = {}
    current_piece = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    next_piece = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    held_piece = None

    score = 0
    lines_cleared = 0
    level = 1
    fall_time = 0
    fall_speed = 0.7
    lines_to_level_up = 5

    # Initialize and play background music
    music = BackgroundMusic("tetris.ogg")
    music.play()
    music.set_volume(0.7)

    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                for row_idx, row in enumerate(current_piece.shape):
                    for col_idx, val in enumerate(row):
                        if val:
                            locked_positions[(current_piece.x + col_idx, current_piece.y + row_idx)] = current_piece.color
                cleared_rows = clear_rows(grid, locked_positions, level)
                if cleared_rows > 0:
                    lines_cleared += cleared_rows
                    score += calculate_score(cleared_rows, level)
                    if lines_cleared // lines_to_level_up > (lines_cleared - cleared_rows) // lines_to_level_up:
                        level += 1
                        fall_speed *= 0.9
                current_piece = next_piece
                next_piece = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
                if not valid_space(current_piece, grid):
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()  # Undo rotation
                if event.key == pygame.K_SPACE:  # Here the indentation was missing
                    # This should be where you drop the piece instantly.
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_ghost_piece(screen, current_piece, grid)
        current_piece.draw(screen)
        draw_score(screen, score, lines_cleared, level)

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    main()
