import curses
import time
from threading import Thread
from os import system
from graphics import Tiles, power_up_tiles, numbers, opening_screen, round_result_screen, tie_screen, score_screen, victory_screen
from game_classes.player_class import make_player1, make_player2
from screen import screen_width, screen_height, tile_height, tile_width, tilemap, randomize_screen

randomize_screen()

system('mode con: cols=91 lines=40')

is_round_over = False
pause_update = False

p1_score = 0
p2_score = 0

player1 = make_player1()
player2 = make_player2()


def round_over(stdscr, winner):
    global player1, player2
    global p1_score, p2_score
    global is_round_over
    global pause_update

    startup_delay = 3
    round_result_delay = 3
    score_screen_delay = 4

    is_round_over = True
    time.sleep(startup_delay)
    pause_update = True

    if winner == "tie":
        for index, value in enumerate(tie_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
    elif winner == "p1":
        p1_score += 1

        for index, value in enumerate(round_result_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        for index, value in enumerate(numbers[1]):
            stdscr.addstr(index + 19, 63, value)
    elif winner == "p2":
        p2_score += 1

        for index, value in enumerate(round_result_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        for index, value in enumerate(numbers[2]):
            stdscr.addstr(index + 19, 63, value)

    stdscr.refresh()
    time.sleep(round_result_delay)

    if p1_score >= 3:
        stdscr.nodelay(False)

        for index, value in enumerate(victory_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        stdscr.refresh()
        while True:
            if stdscr.getch() in [10, 13]:
                break

        for index, value in enumerate(opening_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        for index, value in enumerate(numbers[1]):
            stdscr.addstr(index + 14, 62, value)
        stdscr.refresh()
        while True:
            if stdscr.getch() in [10, 13]:
                break

        stdscr.nodelay(True)

        player1 = make_player1()
        player2 = make_player2()
        randomize_screen()
        p1_score = 0
        p2_score = 0

        is_round_over = False
        pause_update = False
        return
    if p2_score >= 3:
        stdscr.nodelay(False)

        for index, value in enumerate(victory_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        for index, value in enumerate(numbers[2]):
            stdscr.addstr(index + 14, 62, value)
        stdscr.refresh()
        while True:
            if stdscr.getch() in [10, 13]:
                break

        for index, value in enumerate(opening_screen.splitlines()):
            stdscr.addstr(index + tile_height, tile_width, value)
        stdscr.refresh()
        while True:
            if stdscr.getch() in [10, 13]:
                break

        stdscr.nodelay(True)

        player1 = make_player1()
        player2 = make_player2()
        randomize_screen()
        p1_score = 0
        p2_score = 0

        is_round_over = False
        pause_update = False
        return

    for index, value in enumerate(score_screen.splitlines()):
        stdscr.addstr(index + tile_height, tile_width, value)

    for index, value in enumerate(numbers[p1_score]):
        stdscr.addstr(index + 19, 33, value)
    for index, value in enumerate(numbers[p2_score]):
        stdscr.addstr(index + 19, 48, value)

    stdscr.refresh()

    time.sleep(score_screen_delay)

    player1 = make_player1()
    player2 = make_player2()
    randomize_screen()

    is_round_over = False
    pause_update = False


def death_animation(player):
    player.current_tile = Tiles.player_death[0]
    time.sleep(0.32)
    for i in range(1, 4):
        time.sleep(0.16)
        player.current_tile = Tiles.player_death[i]
    time.sleep(0.32)
    for i in range(4, 6):
        time.sleep(0.16)
        player.current_tile = Tiles.player_death[i]


def update_screen(stdscr):
    if not pause_update:
        # updates tilemap on screen
        for y in range(screen_height):
            for x in range(screen_width):
                current_tile = tilemap[y * screen_width + x]
                for z in range(tile_height):
                    if current_tile not in power_up_tiles:
                        stdscr.addstr(y * tile_height + z + tile_height, x * tile_width + tile_width, current_tile[z])
                    else:
                        stdscr.addstr(y * tile_height + z + tile_height, x * tile_width + tile_width, current_tile[z],
                                      curses.A_REVERSE)

        if player1.power_ups["invisibility"] is False:
            for z in range(tile_height):
                stdscr.addstr(player1.y_pos * tile_height + z + tile_height, player1.x_pos * tile_width + tile_width,
                              player1.current_tile[z])

        if player2.power_ups["invisibility"] is False:
            for z in range(tile_height):
                stdscr.addstr(player2.y_pos * tile_height + z + tile_height, player2.x_pos * tile_width + tile_width,
                              player2.current_tile[z])

        stdscr.refresh()


def main(stdscr):
    curses.curs_set(False)

    # adds top and bottom border
    for y in [0, screen_height + 1]:
        for x in range(screen_width + 2):
            for z in range(tile_height):
                stdscr.addstr(y * tile_height + z, x * tile_width, Tiles.block[z])

    # adds left and right border
    for y in range(1, screen_height + 1):
        for x in [0, screen_width + 1]:
            for z in range(tile_height):
                stdscr.addstr(y * tile_height + z, x * tile_width, Tiles.block[z])

    for index, value in enumerate(opening_screen.splitlines()):
        stdscr.addstr(index + tile_height, tile_width, value)
    stdscr.refresh()
    while True:
        if stdscr.getch() in [10, 13]:
            break

    stdscr.nodelay(True)

    update_screen(stdscr)

    while True:
        key = stdscr.getch()
        time.sleep(0.016)
        if not is_round_over:
            if key in [ord("w"), ord("s"), ord("a"), ord("d"), ord(" ")] and player1.moving is False:
                Thread(target=player1.move, args=(key, )).start()

            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT,
                       ord("0")] and player2.moving is False:
                Thread(target=player2.move, args=(key, )).start()

            if tilemap[player1.y_pos * screen_width + player1.x_pos] in [Tiles.bomb_h_blast, Tiles.bomb_v_blast,
                                                                         Tiles.bomb_exploded]:
                if tilemap[player2.y_pos * screen_width + player2.x_pos] in [Tiles.bomb_h_blast, Tiles.bomb_v_blast,
                                                                             Tiles.bomb_exploded]:
                    # If both are dead.
                    Thread(target=death_animation, args=(player1,)).start()
                    Thread(target=death_animation, args=(player2,)).start()
                    Thread(target=round_over, args=(stdscr, "tie")).start()
                else:
                    # If only p1 is dead.
                    Thread(target=death_animation, args=(player1,)).start()
                    Thread(target=round_over, args=(stdscr, "p2")).start()
            elif tilemap[player2.y_pos * screen_width + player2.x_pos] in [Tiles.bomb_h_blast, Tiles.bomb_v_blast,
                                                                           Tiles.bomb_exploded]:
                # If p2 is dead
                Thread(target=death_animation, args=(player2,)).start()
                Thread(target=round_over, args=(stdscr, "p1")).start()
        update_screen(stdscr)


curses.wrapper(main)
