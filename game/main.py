import pygame
from copy import deepcopy
from random import choice, randrange

pygame.init()

W, H = 10, 20
TILE = 29
FPS = 60
field_res = W * TILE, H * TILE
res = 500, 620

figures_pos = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)]
]

anim_count, anim_speed, anim_lim = 0, 60, 2000

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
zero_field = [[0 for i in range(W)] for j in range(H)]

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

sc = pygame.display.set_mode(res)
field = pygame.Surface(field_res)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

get_color = lambda: (randrange(30, 255), randrange(30, 255), randrange(30, 255))
color, next_color = get_color(), get_color()
score_result = 0

main_font = pygame.font.SysFont('impact', 50)
score_font = pygame.font.SysFont('impact', 35)
title = main_font.render('Tetris', True, (200, 150, 0))
score = score_font.render('Score:', True, (200, 50, 125))
record_title = score_font.render('Record:', True, pygame.Color('gold'))


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, Score):
    rec = max(int(record), Score)
    with open('record', 'w') as f:
        f.write(str(rec))


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or zero_field[figure[i].y][figure[i].x]:
        return False
    return True


while True:
    dx = 0
    rotate = False
    record = get_record()

    sc.fill((255, 255, 255))
    sc.blit(field, (20, 20))
    field.fill(pygame.Color('black'))
    sc.blit(title, (330, 20))
    sc.blit(score, (320, 300))
    sc.blit(record_title, (320, 350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx -= 1
            if event.key == pygame.K_RIGHT:
                dx += 1
            if event.key == pygame.K_DOWN:
                anim_lim = 200
            if event.key == pygame.K_UP:
                rotate = True

    # горизонтальное смещение
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = figure_old
            break

    # вертикальное смещение
    anim_count += anim_speed
    if anim_count > anim_lim:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    zero_field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_lim = 2000
                break

    # поворот
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = figure_old
                break

    # рисуем сетку
    [pygame.draw.rect(field, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # рисуем фигуру
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(field, color, figure_rect)

    # рисуем следующую фигуру
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 260
        figure_rect.y = next_figure[i].y * TILE + 100
        pygame.draw.rect(field, color, figure_rect)
        pygame.draw.rect(sc, next_color, figure_rect)

    # удаление полной линии
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if zero_field[row][i]:
                count += 1
            zero_field[line][i] = zero_field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    score_result += lines
    set_record(record, score_result)
    record = get_record()
    sc.blit(score_font.render(str(score_result), True, (200, 50, 125)), (440, 300))
    sc.blit(score_font.render(record, True, pygame.Color('gold')), (440, 350))

    #  рисуем поле
    for y, raw in enumerate(zero_field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(field, col, figure_rect)

    # концовка игры
    for i in range(W):
        if zero_field[0][i]:
            set_record(record, score_result)
            zero_field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_lim = 0, 60, 2000
            score_result = 0
            for i_rect in grid:
                pygame.draw.rect(field, get_color(), i_rect)
                sc.blit(field, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
