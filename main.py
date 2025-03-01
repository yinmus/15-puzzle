import pygame
import random
import sys

pygame.init()

SCREEN_SIZE = 500
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
FONT = pygame.font.Font(None, 40)
BUTTON_FONT = pygame.font.Font(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (0, 150, 255)
HIGHLIGHT_COLOR = (100, 200, 255)

def gen():
    numbers = list(range(1, 16)) + [0]
    random.shuffle(numbers)
    return [numbers[i:i+4] for i in range(0, 16, 4)]

def draw_puzzle(screen, puzzle):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * TILE_SIZE, row * TILE_SIZE + 50
            num = puzzle[row][col]
            pygame.draw.rect(screen, WHITE if num else GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
            if num:
                text = FONT.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)

def restart_btn(screen, hover):
    color = HIGHLIGHT_COLOR if hover else BUTTON_COLOR
    button_rect = pygame.Rect(SCREEN_SIZE // 2 - 80, 10, 160, 40)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    text = BUTTON_FONT.render("(R) Restart", True, WHITE)
    screen.blit(text, text.get_rect(center=button_rect.center))

def find_empty(puzzle):
    for i, row in enumerate(puzzle):
        if 0 in row:
            return i, row.index(0)

def move_tile(puzzle, from_pos, to_pos):
    puzzle[from_pos[0]][from_pos[1]], puzzle[to_pos[0]][to_pos[1]] = puzzle[to_pos[0]][to_pos[1]], puzzle[from_pos[0]][from_pos[1]]

def is_adjacent(tile_pos, empty_pos):
    return abs(tile_pos[0] - empty_pos[0]) + abs(tile_pos[1] - empty_pos[1]) == 1

def check_win(puzzle):
    return [num for row in puzzle for num in row] == list(range(1, 16)) + [0]

def play_game():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("15 Puzzle")
    puzzle = gen()

    while True:
        screen.fill(BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_restart = SCREEN_SIZE // 2 - 80 <= mouse_x <= SCREEN_SIZE // 2 + 80 and 10 <= mouse_y <= 50
        restart_btn(screen, hover_restart)
        draw_puzzle(screen, puzzle)
        
        if check_win(puzzle):
            text = FONT.render("Win!", True, WHITE)
            screen.blit(text, (SCREEN_SIZE // 2 - 40, SCREEN_SIZE // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if hover_restart:
                    puzzle = gen()
                elif 50 <= y < SCREEN_SIZE:
                    col, row = x // TILE_SIZE, (y - 50) // TILE_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        clicked_pos = (row, col)
                        empty_pos = find_empty(puzzle)
                        if is_adjacent(clicked_pos, empty_pos):
                            move_tile(puzzle, clicked_pos, empty_pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                puzzle = gen()

if __name__ == "__main__":
    play_game()
