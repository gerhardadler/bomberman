import random
from graphics import Tiles

screen_height = 11
screen_width = 13

tile_height = 3
tile_width = 6

# create tilemap

tilemap = []


def randomize_screen():
    global tilemap
    tilemap.clear()
    for y in range(screen_height):
        for x in range(screen_width):
            if y % 2 == 1 and x % 2 == 1:
                tilemap.append(Tiles.block)
            elif y in [0, 1] and x in [0, 1] or y in [screen_height - 2, screen_height - 1] and x in [screen_width - 2,
                                                                                                      screen_width - 1]:
                tilemap.append(Tiles.none)
            elif random.randrange(4) == 3:
                tilemap.append(Tiles.none)
            else:
                tilemap.append(Tiles.brick)
