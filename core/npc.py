class NPC:
    def __init__(self, name, dialogue, gift):
        self.name = name
        self.dialogue = dialogue
        self.gift = gift
        self.given = False

    def talk(self, player):
        print(self.dialogue)

        if not self.given:
            player.inventory.append(self.gift)
            self.given = True
            print("You got:", self.gift)