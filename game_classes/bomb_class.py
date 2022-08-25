import curses
import time
import random

from graphics import Tiles, power_up_tiles
from screen import screen_width, screen_height, tilemap


class Bomb:

    def __init__(self, x, y, placer):
        self.x_pos = x
        self.y_pos = y
        self.placer = placer

    def place(self):
        tile_index = self.y_pos * screen_width + self.x_pos
        tilemap[tile_index] = Tiles.bomb_tile
        for i in range(50):
            time.sleep(0.06)
            if tilemap[tile_index] == Tiles.bomb_exploded:
                break
        curses.flash()
        tilemap[tile_index] = Tiles.bomb_exploded

        self.placer.bombs_placed -= 1

        bomb_range = range(1, self.placer.power_ups["bomb_radius"] + 1)

        h_blasted = []
        v_blasted = []
        for z in [-1, 1, screen_width * -1, screen_width]:
            for i in bomb_range:
                if z in [-1, 1] and tile_index // screen_width != (
                        tile_index + i * z) // screen_width or tile_index + i * z < 0:
                    break
                if z in [screen_width * -1, screen_width] and (tile_index + i * z) // screen_width == screen_height:
                    break
                if tilemap[tile_index + i * z] in [Tiles.none, Tiles.bomb_h_blast, Tiles.bomb_v_blast]:
                    if z in [-1, 1]:
                        h_blasted.append((tile_index + i * z, Tiles.none))
                    else:
                        v_blasted.append((tile_index + i * z, Tiles.none))
                elif tilemap[tile_index + i * z] in power_up_tiles:
                    if z in [-1, 1]:
                        h_blasted.append((tile_index + i * z, Tiles.none))
                    else:
                        v_blasted.append((tile_index + i * z, Tiles.none))
                    break
                elif tilemap[tile_index + i * z] == Tiles.brick:
                    if z in [-1, 1]:
                        h_blasted.append((tile_index + i * z, Tiles.brick))
                    else:
                        v_blasted.append((tile_index + i * z, Tiles.brick))
                    break
                elif tilemap[tile_index + i * z] == Tiles.bomb_tile:
                    tilemap[tile_index + i * z] = Tiles.bomb_exploded
                    break
                else:
                    break

        for i in h_blasted:
            tilemap[i[0]] = Tiles.bomb_h_blast
        for i in v_blasted:
            tilemap[i[0]] = Tiles.bomb_v_blast
        time.sleep(0.5)

        if self.placer.power_ups["luck"] >= 0:
            self.placer.power_ups["luck"] = -3

        for i in h_blasted:
            if i[1] == Tiles.brick:
                if random.randrange(self.placer.power_ups["luck"] * -1) == 0:
                    tilemap[i[0]] = random.choice(power_up_tiles)
                else:
                    tilemap[i[0]] = Tiles.none
            else:
                tilemap[i[0]] = Tiles.none
        for i in v_blasted:
            if i[1] == Tiles.brick:
                if random.randrange(self.placer.power_ups["luck"] * -1) == 0:
                    tilemap[i[0]] = random.choice(power_up_tiles)
                else:
                    tilemap[i[0]] = Tiles.none
            else:
                tilemap[i[0]] = Tiles.none
        tilemap[self.y_pos * screen_width + self.x_pos] = Tiles.none
