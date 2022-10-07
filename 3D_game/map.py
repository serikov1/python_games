from settings import *

text_map = [
    '11111111111111111111',
    '1...2..............1',
    '122....222.........1',
    '1..............22..1',
    '1.....2222.........1',
    '1.....2222.....2...1',
    '1.2................1',
    '1.....222222222....1',
    '1.....222222.......1',
    '1..2...........22..1',
    '1.......2......22..1',
    '11111111111111111111',
]

world_map = {}
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'

