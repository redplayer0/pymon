class Trainer:
    def __init__(self, name, spr):
        self.name = name
        self.spr = spr
        self.x = 0
        self.tx = 0
        self.y = 0
        self.ty = 0
        self.under = ""
        self.party = []
        self.items = []
        self.money = 0
        self.state = "walk"

    def set_window(self, win):
        self.win = win

    def set_world(self, world):
        self.world = world

    def move(self, y, x, tile_type):
        if self.state == "talk":
            return
        # Replace player with the tile under him
        self.world.put_at(self.y, self.x, self.under)
        
        # Update player's position
        self.x = x
        self.y = y

        # Update tile under player
        self.under = tile_type
        # Render player
        self.world.put_at(self.y, self.x, self.spr)
        self.world.refresh()
    
    def spawn(self, y, x):
        self.x = x
        self.y = y
        self.under = self.world.get_from(y, x)
        self.world.put_at(y, x, self.spr)
        self.world.refresh()
