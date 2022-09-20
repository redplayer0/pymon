import curses
from mapdata import data
from trainer import Trainer

class Game:
    # blocks = ["#", "_", "|", "=", "$", "^"]
    max_y = 13
    max_x = 13

    def __init__(self):
        self.running = True
        self.frames = 0
        # Set lastkey to empty
        self.lastkey = ""
        # Map related
        self.curmap = ""
        self.previousmap = ""

    def add_player(self, player):
        self.player = player
        self.player.world = self
        self.player.win = self.stdscr

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(False)
        self.stdscr.clear()

    def put_at(self, y, x, text):
        self.stdscr.addstr(y, x*2, text)

    def _getkey(self):
        try:
            return self.stdscr.getkey()
        except:
            return ""

    def getkey(self):
        self.lastkey = self._getkey()

    def get_from(self, y, x):
        return chr(self.stdscr.inch(y, x*2))

    def delete_ln(self, line):
        self.stdscr.move(line, 0)
        self.stdscr.deleteln()

    def load_map(self, mapname):
        self.previousmap = self.curmap
        self.curmap = mapname
        with open("pallet", "r") as f:
            map_found = False
            y = 0
            for line in f.readlines():
                if "end" in line and map_found:
                    break
                if map_found:
                    self.stdscr.addstr(y, 0, line)
                    y += 1
                if mapname in line:
                    map_found = True

        self.refresh()

    def check_tile(self):
        k = self.lastkey
        x = self.player.x
        y = self.player.y
        match k:
            case "d":
                x += 1
            case "a":
                x -= 1
            case "w":
                y -= 1
            case "s":
                y += 1

        tile_type = self.get_from(y, x)
        tile = (y, x)

        if tile_type == "$":
            txt = data[self.curmap][tile_type][tile]
            self.put_at(15, 0, txt)
        elif tile_type == ".":
            self.player.move(y, x, tile_type)
            self.delete_ln(15)
        elif tile in data[self.curmap]["warps"]:
            self.warp_player(tile)
        elif tile_type in data[self.curmap]["npcs"]:
            self.dialog(data[self.curmap]["npcs"][tile_type])

    def warp_player(self, tile):
        target = data[self.curmap]["warps"][tile]
        self.load_map(target[0])
        self.player.spawn(target[1][0], target[1][1])

    def dialog(self, text):
        self.player.state = "talk"
        top = 15
        bot = 16
        lines = len(text) - 1
        i = 0
        while i <= lines:
            self.put_at(top, 0, text[i])
            if i+1 <= lines:
                self.put_at(bot, 0, text[i+1])
            self.refresh()
            self.getkey()
            if self.lastkey:
                self.delete_ln(top)
                self.delete_ln(bot)
                i += 1
        self.player.state = "walk"
        self.delete_ln(top)
        self.delete_ln(bot)

    def handle_input(self):
        k = self.lastkey
        if k in ["w", "a", "s", "d"]:
            self.check_tile()
        elif k == "q":
            self.running = False
            curses.curs_set(1)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    def refresh(self):
        self.put_at(0, 15, f"x: {self.player.x} y: {self.player.y}")
        self.put_at(14, 0, str(self.frames))
        self.put_at(14, 10, self.player.state)
        self.frames += 1
        self.stdscr.refresh()
        curses.napms(30)


world = Game()     
world.init_curses()
player = Trainer("red", "@")
world.add_player(player)
world.load_map("pallet")
world.player.spawn(4, 4)



while True:
    world.getkey()
    if not world.running:
        break
    world.handle_input()
    world.refresh()
