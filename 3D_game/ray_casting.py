import pygame
from settings import *
from map import world_map


# def ray_casting(sc, player_pos, player_angle):
#     cur_angle = player_angle - HALF_FOV
#     xo, yo = player_pos
#     for ray in range(NUM_RAYS):
#         sin_a = math.sin(cur_angle)
#         cos_a = math.cos(cur_angle)
#         for depth in range(MAX_DEPTH):
#             x = xo + depth * cos_a
#             y = yo + depth * sin_a
#             # pygame.draw.line(sc, DARKGREY, player_pos, (x, y), 2)
#             if (x // TILE * TILE, y // TILE * TILE) in world_map:
#                 depth *= math.cos(player_angle - cur_angle)
#                 proj_height = PROJ_COEFF / depth
#                 c = 255 / (1 + depth * depth * 0.00002)
#                 color = (c, c // 2, c // 3)
#                 pygame.draw.rect(sc, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
#                 break
#         cur_angle += DELTA_ANGLE


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(player, textures):
    walls = []
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    for ray in range(NUM_RAYS):
        cos_a = math.cos(cur_angle)
        sin_a = math.sin(cur_angle)

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # horizontal
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)

        # c = 255 / (1 + depth * depth * 0.00002)
        # color = (c, c // 2, c // 3)
        # pygame.draw.rect(sc, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
        cur_angle += DELTA_ANGLE

    return walls
