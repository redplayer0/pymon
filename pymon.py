import curses
from curses import wrapper

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(True)
stdscr.keypad(False)

def set_map(screen, mapname):
    screen = screen
    with open(mapname, "r") as f:
        for y, line in enumerate(f.readlines()):
            screen.addstr(y, 0, line)
    def inner(mapname):
        with open(mapname, "r") as f:
            for y, line in enumerate(f.readlines()):
                screen.addstr(y, 0, line)
    return inner


def _getkey(screen):
    screen = screen
    def inner():
        try:
            return screen.getkey()
        except:
            return ""
    return inner


def setup_player(screen, y, x):
    screen = screen
    player = "@"
    previous = chr(screen.inch(y, x*2))
    screen.addstr(y, x*2, player)
    sx = x*2
    sy = y
    def inner(y, x):
        nonlocal previous, sx, sy
        screen.addstr(sy, sx, previous)
        sy = sy + y
        sx = sx + x*2
        previous = chr(screen.inch(sy, sx))
        screen.addstr(sy, sx, player)
    return inner


def main(stdscr):
    loadmap = set_map(stdscr, "pallet")
    move_to = setup_player(stdscr, 0, 0)
    getkey = _getkey(stdscr)

    keys = []

    while True:
        key = getkey()
        if key == "q":
            break
        if key == "d":
            move_to(0,1)
        elif key == "a":
            move_to(0,-1)
        elif key == "w":
            move_to(-1,0)
        elif key == "s":
            move_to(1,0)

        if key is not "":
            keys.append(key)

        stdscr.addstr(15, 0, " ".join(keys))
        stdscr.refresh()
        curses.napms(100)


wrapper(main)
