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
    puzzle = [numbers[i:i+4] for i in range(0, 16, 4)]
    return puzzle

def draw_puzzle(screen, puzzle):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * TILE_SIZE, row * TILE_SIZE + 50
            num = puzzle[row][col]
            if num != 0:
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
                text = FONT.render(str(num), True, BLACK)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)

def restart_btn(screen):
    button_rect = pygame.Rect(SCREEN_SIZE // 2 - 80, 10, 160, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)
    text = BUTTON_FONT.render("(R) Restart", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def fe(puzzle):
    for i, row in enumerate(puzzle):
        if 0 in row:
            return i, row.index(0)

def move_tile(puzzle, from_pos, to_pos):
    x1, y1 = from_pos
    x2, y2 = to_pos
    puzzle[x1][y1], puzzle[x2][y2] = puzzle[x2][y2], puzzle[x1][y1]

def Ia(puzzle, tile_pos, empty_pos):
    x1, y1 = tile_pos
    x2, y2 = empty_pos
    return abs(x1 - x2) + abs(y1 - y2) == 1

def check_win(puzzle):
    goal = list(range(1, 16)) + [0]
    return [num for row in puzzle for num in row] == goal

def play_game():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("sudoku")
    puzzle = gen()

    while True:
        screen.fill(BLACK)
        restart_btn(screen)
        draw_puzzle(screen, puzzle)

        if check_win(puzzle):
            text = FONT.render("Win!", True, WHITE)
            screen.blit(text, (50, SCREEN_SIZE // 2 - 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if SCREEN_SIZE // 2 - 80 <= x <= SCREEN_SIZE // 2 + 80 and 10 <= y <= 50:
                    puzzle = gen()

                else:
                    col, row = x // TILE_SIZE, (y - 50) // TILE_SIZE
                    clicked_pos = (row, col)

                    empty_pos = fe(puzzle)

                    if Ia(puzzle, clicked_pos, empty_pos):
                        move_tile(puzzle, clicked_pos, empty_pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    puzzle = gen()

if __name__ == "__main__":
    play_game()
