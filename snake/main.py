import pygame
import random

pygame.init()
# ширина и высота окна и игрового поля
w_d, h_d = 800, 600
W, H = 800, 400
# создание окна
display = pygame.display.set_mode((w_d, h_d))
# создание поля
field = pygame.Surface((W, H))
# подпись окна
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


# функция вывода сообщения
def message(msg, color, font_size, x_coord, y_coord):
    font_style = pygame.font.SysFont(None, font_size)
    mes = font_style.render(msg, True, color)
    mes_rect = mes.get_rect(center=(x_coord, y_coord))
    display.blit(mes, mes_rect)


# шрифты
score_font = pygame.font.SysFont('Comic Sans MS', 30)
quit_text = score_font.render('EXIT', True, (255, 255, 255))
continue_text = score_font.render('RESTART', True, (255, 255, 255))


# функция вывода результата
def score(res):
    mes = score_font.render('Score:' + str(res), True, white)
    score_rect = mes.get_rect(center=(W / 2, 50))
    display.blit(mes, score_rect)


# цвета
blue = (0, 0, 255)
orange = (255, 150, 0)
green = (0, 255, 0)
black = (0, 0, 0)
color = (200, 0, 255)
white = (255, 255, 255)
fps = 60

# ширина блока, скорость, массив змеи, длина змеи(для проверки)
block = 20
snake_speed = 10


# основная фунция
def game_loop():
    # координаты еды
    apple_x = round(random.randint(0, W - block) / block) * block
    apple_y = round(random.randint(0, H - block) / block) * block

    # основной цикл игры
    game_over = True
    game_close = False

    # начальные данные
    x = W / 2
    y = H / 2
    x_change = 0
    y_change = 0
    snake_list = []
    length = 1

    while game_over:
        clock.tick(snake_speed)

        while game_close:
            # отрисовка окна завершения игры
            display.fill(blue)

            message('Game over!', white, 60, w_d / 2, h_d / 2 - 200)
            message('Your result: ' + str(length - 1), white, 40, w_d / 2, h_d / 2 - 100)

            pygame.draw.rect(display, green, [w_d / 2 - 90, h_d / 2 + 60, 180, 70])
            quit_text_rect = quit_text.get_rect(center=(w_d / 2, h_d / 2 + 95))

            pygame.draw.rect(display, green, [w_d / 2 - 90, h_d / 2 + 140, 180, 70])
            continue_text_rect = continue_text.get_rect(center=(w_d / 2, h_d / 2 + 175))

            display.blit(quit_text, quit_text_rect)
            display.blit(continue_text, continue_text_rect)

            pygame.display.update()

            # обработка действий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_close = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if w_d / 2 - 90 <= mouse[0] <= w_d / 2 + 90 and h_d / 2 + 60 <= mouse[1] <= h_d / 2 + 130:
                        game_over = False
                        game_close = False
                    if w_d / 2 - 90 <= mouse[0] <= w_d / 2 + 90 and h_d / 2 + 140 <= mouse[1] <= h_d / 2 + 210:
                        game_loop()

        # проверка нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and x_change == 0:
                    x_change = - block
                    y_change = 0
                elif event.key == pygame.K_d and x_change == 0:
                    x_change = block
                    y_change = 0
                elif event.key == pygame.K_w and y_change == 0:
                    y_change = - block
                    x_change = 0
                elif event.key == pygame.K_s and y_change == 0:
                    y_change = block
                    x_change = 0

        # проверка выхода за границы
        if x >= W or x <= 0 or y >= H or y <= 0:
            game_close = True

        # изменение координат головы змеи
        x += x_change
        y += y_change

        # отрисовка поля
        display.fill(green)
        display.blit(field, (0, 100))
        field.fill(white)

        # отрисовка еды
        pygame.draw.circle(field, orange, [apple_x + block / 2, apple_y + block / 2], int(block / 2))

        # проверка длины змеи
        snake_body = [x, y]
        snake_list.insert(0, snake_body)
        if len(snake_list) > length:
            del snake_list[-1]

        # проверка самопересечения
        snake_head = snake_list[0]
        for elem in snake_list[-1]:
            if elem == snake_head:
                game_close = True

        # отрисовка змеи
        for coord in snake_list:
            if coord == snake_list[0]:
                pygame.draw.rect(field, color, [coord[0], coord[1], block, block])
            else:
                pygame.draw.rect(field, blue, [coord[0], coord[1], block, block])

        # удаление еды
        if x == apple_x and y == apple_y:
            apple_x = round(random.randint(0, W - block) / block) * block
            apple_y = round(random.randint(0, H - block) / block) * block
            length += 1

        score(length - 1)

        pygame.display.flip()


game_loop()
