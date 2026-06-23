import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4


BG_COLOR = (245, 245, 245)          
BOARD_COLOR = (255, 255, 255)      
LINE_COLOR = (200, 200, 200)       
CROSS_COLOR = (50, 50, 50)          
CIRCLE_COLOR = (70, 130, 180)       
HIGHLIGHT_COLOR = (255, 215, 0)   
TEXT_COLOR = (30, 30, 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")
font = pygame.font.Font(None, 60)

board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
current_player = 1  # 1 – игрок, 2 – компьютер
game_over = False
winner = None

def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
            elif board[row][col] == 2:
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    if all(board[i][j] != 0 for i in range(3) for j in range(3)):
        return 0
    return None

def computer_move_random():
    """Случайный ход компьютера."""
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2
        return True
    return False

def reset_game():
    global board, current_player, game_over, winner
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = 1
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

def draw_text(text, color, y_offset=0):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)

# Старт
screen.fill(BG_COLOR)
draw_lines()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 1:
            x, y = event.pos
            col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == 0:
                board[row][col] = 1
                draw_figures()
                pygame.display.update()
                winner = check_winner()
                if winner is not None:
                    game_over = True
                else:
                    current_player = 2

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    # Ход компьютера
    if not game_over and current_player == 2:
        computer_move_random()
        draw_figures()
        pygame.display.update()
        winner = check_winner()
        if winner is not None:
            game_over = True
        else:
            current_player = 1

    # Вывод сообщений
    if not game_over:
        if current_player == 1:
            draw_text("Ваш ход (крестик)", TEXT_COLOR, -200)
        else:
            draw_text("Ход компьютера...", TEXT_COLOR, -200)
    else:
        if winner == 1:
            draw_text("Вы выиграли! ", (0, 255, 0), -100)
        elif winner == 2:
            draw_text("Компьютер выиграл! ", (255, 0, 0), -100)
        else:
            draw_text("Ничья!", (255, 255, 0), -100)
        draw_text("Нажмите R для новой игры", TEXT_COLOR, 60)

    pygame.display.update()