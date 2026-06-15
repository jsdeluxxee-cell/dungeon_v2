from core.monster import Monster

class Moo(Monster):
    def __init__(self):
        super().__init__("mo'o", 60, 15, "The mo'o strikes from the water!")

    def attack(self, player):
        if "spear" not in player.inventory and "fishhook" not in player.inventory:
            print("The mo'o drags you underwater!")
            player.take_damage(self.damage + 10, self.name)
        else:
            super().attack(player)