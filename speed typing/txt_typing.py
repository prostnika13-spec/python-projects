import pygame
from pygame.locals import *
import sys
import time
import random

class Game:

    def __init__(self):
        self.w = 750
        self.h = 500
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Время:0 Правильность:0 % кол-во символов:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        pygame.init()

        # Загрузка изображений (все в формате JPG)
        self.open_img = pygame.image.load('end.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (500, 750))

        # Иконка теперь тоже JPG (было PNG)
        self.time_img = pygame.image.load('icon.jpg')
        self.time_img = pygame.transform.scale(self.time_img, (150, 150))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Тест скорости печати')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        # Здесь можно загружать предложения из файла или использовать список
        sentences = [
            "The quick brown fox jumps over the lazy dog",
            "Python is a powerful programming language",
            "Practice makes perfect when learning to type",
            "Typing speed tests are fun and useful"
        ]
        return random.choice(sentences)

    def show_results(self, screen):
        if not self.end:
            self.total_time = time.time() - self.time_start
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except IndexError:
                    pass
            self.accuracy = count / len(self.word) * 100 if self.word else 0
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time) if self.total_time > 0 else 0
            self.end = True

            self.results = (f'Время: {round(self.total_time)} сек  '
                            f'Точность: {round(self.accuracy)}%  '
                            f'Символов: {len(self.input_text)}  '
                            f'WPM: {round(self.wpm)}')

            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))
            self.draw_text(screen, self.results, 350, 28, self.RESULT_C)
            pygame.display.update()

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)

        self.end = False
        self.input_text = ''
        self.word = self.get_sentence()
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.draw_text(self.screen, "Тест скорости печати", 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)
        pygame.display.update()

    def run(self):
        self.reset_game()
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # Клик по полю ввода
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    # Клик по кнопке Reset (после завершения)
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.reset_game()
                        self.end = False  # сбрасываем флаг окончания

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.show_results(self.screen)
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            if event.unicode.isprintable():
                                self.input_text += event.unicode

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Game().run()