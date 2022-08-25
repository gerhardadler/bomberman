import curses
import time

from graphics import Tiles, power_up_tiles
from game_classes.bomb_class import Bomb
from screen import screen_width, screen_height, tilemap


class Player:

    bombs_placed = 0
    speed = 0.05
    moving = False
    current_tile = Tiles.player_tile

    def __init__(self, name, x, y, power_ups):
        self.name = name
        self.x_pos = x
        self.y_pos = y
        self.power_ups = power_ups

    def move(self, key):
        x = 0
        y = 0

        if key in [ord("w"), curses.KEY_UP]:
            y = -1
        elif key in [ord("s"), curses.KEY_DOWN]:
            y = 1
        elif key in [ord("a"), curses.KEY_LEFT]:
            x = -1
        elif key in [ord("d"), curses.KEY_RIGHT]:
            x = 1
        if key in [ord(" "), ord("0")]:
            if tilemap[self.y_pos * screen_width + self.x_pos] == Tiles.none:
                if self.bombs_placed < self.power_ups["bomb_cap"]:
                    self.bombs_placed += 1
                    new_bomb = Bomb(self.x_pos, self.y_pos, self)
                    new_bomb.place()

        new_pos = (self.y_pos + y) * screen_width + self.x_pos + x
        # nesting ifs to let it make sense. Ugly, though better than one line that goes way longer than this one.
        if tilemap[new_pos] not in [Tiles.block, Tiles.brick, Tiles.bomb_tile]:
            if not (x == -1 and self.x_pos % screen_width == 0):
                if not (x == 1 and (self.x_pos + 1) % screen_width == 0):
                    if not (y == -1 and self.y_pos == 0):
                        if not (y == 1 and self.y_pos == screen_height):
                            self.moving = True
                            self.x_pos += x
                            self.y_pos += y
                            power_up_list = ["bomb_radius", "luck", "invisibility", "bomb_cap"]
                            if tilemap[new_pos] in power_up_tiles:
                                for i in range(len(power_up_tiles)):
                                    if tilemap[new_pos] == power_up_tiles[i]:
                                        self.power_ups[power_up_list[i]] += 1
                                        tilemap[new_pos] = Tiles.none
                            time.sleep(self.speed)
                            self.moving = False
                            if self.power_ups["invisibility"] is not False:
                                time.sleep(4)
                                self.power_ups["invisibility"] = False


def make_player1():
    return Player(
        "player1",
        0,
        0,
        {
            "bomb_radius": 1,
            "luck": -5,
            "invisibility": False,
            "bomb_cap": 1
        }
    )


def make_player2():
    return Player(
        "player2",
        screen_width - 1,
        screen_height - 1,
        {
            "bomb_radius": 1,
            "luck": -5,
            "invisibility": False,
            "bomb_cap": 1
        }
    )
