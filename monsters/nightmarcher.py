from core.monster import Monster

class Nightmarcher(Monster):
    def __init__(self):
        super().__init__("Nightmarcher", 70, 19, "The Nightmarcher attacks!")
        self.turn = 0

    def attack(self, player):
        self.turn += 1
        if self.turn % 2 == 0:
            print("The Nightmarcher passes through you... (miss)")
            return
        super().attack(player)