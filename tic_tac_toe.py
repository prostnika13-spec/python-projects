import pygame
import sys
import random
import math

pygame.init()

WIDTH = 600
HEIGHT = 700
TOP_OFFSET = 140              # высота верхней панели

BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 12
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

BG_COLOR = (240, 240, 240)
PANEL_COLOR = (45, 45, 65)
BOARD_COLOR = (255, 255, 255)
LINE_COLOR = (200, 200, 200)
CROSS_COLOR = (40, 40, 40)
CIRCLE_COLOR = (60, 130, 190)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 150, 220)
BUTTON_HOVER = (130, 180, 250)
BUTTON_ACTIVE = (60, 100, 160)
WIN_COLOR = (255, 215, 0)

# Шрифты
font_large = pygame.font.Font(None, 50)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 28)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
current_player = 1          # 1 – игрок (крестик), 2 – компьютер (нолик)
game_over = False
winner = None
difficulty = 0            

def draw_panel():
    """Рисует верхнюю панель с фоном и разделительной линией."""
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, TOP_OFFSET))
    pygame.draw.line(screen, (80, 80, 100), (0, TOP_OFFSET), (WIDTH, TOP_OFFSET), 3)

def draw_button(text, x, y, w, h, color, text_color=TEXT_COLOR, border_radius=10):
    """Рисует кнопку с текстом."""
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=border_radius)
    surf = font_medium.render(text, True, text_color)
    rect = surf.get_rect(center=(x + w//2, y + h//2))
    screen.blit(surf, rect)

def draw_status(message, color=TEXT_COLOR):
    """Выводит статус игры в центре панели."""
    surf = font_large.render(message, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, TOP_OFFSET // 2 - 5))
    screen.blit(surf, rect)

def draw_board():
    """Рисует игровое поле (фон + сетка + фигуры)."""
    pygame.draw.rect(screen, BOARD_COLOR, (0, TOP_OFFSET, WIDTH, HEIGHT - TOP_OFFSET))
    draw_lines()
    draw_figures()

def draw_lines():
    """Рисует сетку 3x3 со смещением вниз."""
    for i in range(1, 3):
        # Вертикальные линии
        x = i * SQUARE_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, TOP_OFFSET), (x, TOP_OFFSET + 3 * SQUARE_SIZE), LINE_WIDTH)
        # Горизонтальные линии
        y = TOP_OFFSET + i * SQUARE_SIZE
        pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)

def draw_figures():
    """Рисует все крестики и нолики."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x = col * SQUARE_SIZE
            y = TOP_OFFSET + row * SQUARE_SIZE
            if board[row][col] == 1:      # крестик
                pygame.draw.line(screen, CROSS_COLOR,
                                 (x + SPACE, y + SPACE),
                                 (x + SQUARE_SIZE - SPACE, y + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (x + SPACE, y + SQUARE_SIZE - SPACE),
                                 (x + SQUARE_SIZE - SPACE, y + SPACE),
                                 CROSS_WIDTH)
            elif board[row][col] == 2:    # нолик
                center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_ui():
    """Отрисовывает всю графику (панель, кнопки, доску, статус)."""
    screen.fill(BG_COLOR)
    draw_panel()
    draw_board()

    # Кнопка "Новая игра" (справа)
    new_game_rect = pygame.Rect(WIDTH - 160, 15, 130, 45)
    draw_button("Новая игра", new_game_rect.x, new_game_rect.y, new_game_rect.w, new_game_rect.h, BUTTON_COLOR)

    # Кнопки сложности (слева)
    easy_rect = pygame.Rect(20, 15, 100, 45)
    hard_rect = pygame.Rect(130, 15, 100, 45)
    # Активная кнопка выделяется
    easy_color = BUTTON_ACTIVE if difficulty == 0 else BUTTON_COLOR
    hard_color = BUTTON_ACTIVE if difficulty == 1 else BUTTON_COLOR
    draw_button("Лёгкий", easy_rect.x, easy_rect.y, easy_rect.w, easy_rect.h, easy_color)
    draw_button("Сложный", hard_rect.x, hard_rect.y, hard_rect.w, hard_rect.h, hard_color)

    # Статус
    if not game_over:
        if current_player == 1:
            draw_status("Ваш ход (крестик)")
        else:
            draw_status("Ход компьютера...", (200, 200, 200))
    else:
        if winner == 1:
            draw_status("Вы выиграли!", (0, 255, 0))
        elif winner == 2:
            draw_status("Компьютер выиграл!", (255, 80, 80))
        else:
            draw_status("Ничья!", (255, 255, 0))
        # Маленькая подсказка (опционально)
        hint = font_small.render("Нажмите R или кнопку «Новая игра»", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, TOP_OFFSET - 30))

    pygame.display.update()

# ------------------- Логика игры -------------------
def check_winner():
    """Возвращает 1, 2, 0 (ничья) или None."""
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

def minimax(board, depth, is_maximizing):
    """
    Минимакс для сложного режима.
    Возвращает оценку: +10 - победа компьютера (нолики), -10 - победа игрока (крестики), 0 - ничья.
    """
    result = check_winner()
    if result == 2:
        return 10 - depth
    elif result == 1:
        return -10 + depth
    elif result == 0:
        return 0

    if is_maximizing:   # ход компьютера (нолики)
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = 2
                    score = minimax(board, depth + 1, False)
                    board[r][c] = 0
                    best = max(score, best)
        return best
    else:               # ход игрока (крестики)
        best = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    board[r][c] = 1
                    score = minimax(board, depth + 1, True)
                    board[r][c] = 0
                    best = min(score, best)
        return best

def computer_move():
    """Выполняет ход компьютера в зависимости от выбранной сложности."""
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]
    if not empty:
        return False

    if difficulty == 0:   
        r, c = random.choice(empty)
        board[r][c] = 2
        return True
    else:               
        best_score = -math.inf
        best_move = None
        for r, c in empty:
            board[r][c] = 2
            score = minimax(board, 0, False)
            board[r][c] = 0
            if score > best_score:
                best_score = score
                best_move = (r, c)
        if best_move:
            board[best_move[0]][best_move[1]] = 2
            return True
        return False

def reset_game():
    """Сбрасывает игровое поле, оставляя сложность и счёт (если есть)."""
    global board, current_player, game_over, winner
    board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = 1
    game_over = False
    winner = None

clock = pygame.time.Clock()
running = True

draw_ui()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Проверка клика по кнопке "Новая игра"
            if WIDTH - 160 <= mouse_x <= WIDTH - 30 and 15 <= mouse_y <= 60:
                reset_game()
                draw_ui()
                continue

            # Проверка клика по кнопкам сложности
            if 20 <= mouse_x <= 120 and 15 <= mouse_y <= 60:
                if difficulty != 0:
                    difficulty = 0
                    draw_ui()   # обновляем панель
                continue
            if 130 <= mouse_x <= 230 and 15 <= mouse_y <= 60:
                if difficulty != 1:
                    difficulty = 1
                    draw_ui()
                continue

            # Если клик по доске и игра не окончена, и ход игрока
            if not game_over and current_player == 1:
                # Проверяем, что клик попал в область доски (ниже TOP_OFFSET)
                if mouse_y > TOP_OFFSET:
                    col = mouse_x // SQUARE_SIZE
                    row = (mouse_y - TOP_OFFSET) // SQUARE_SIZE
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == 0:
                        board[row][col] = 1
                        winner = check_winner()
                        if winner is not None:
                            game_over = True
                        else:
                            current_player = 2
                        draw_ui()   # отображаем ход игрока

        # Клавиша R для новой игры
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            draw_ui()

    if not game_over and current_player == 2:
        pygame.time.delay(300)
        computer_move()
        winner = check_winner()
        if winner is not None:
            game_over = True
        else:
            current_player = 1
        draw_ui()

    clock.tick(30)

pygame.quit()