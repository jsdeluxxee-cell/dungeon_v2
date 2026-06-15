class Room:
    def __init__(self, description, exits, item=None, npc=None, monster=None):
        self.description = description
        self.exits = exits
        self.item = item
        self.npc = npc
        self.monster = monster

    def describe(self):
        print("\n" + self.description)

        if self.item:
            print("You see:", self.item)

        if self.monster and self.monster.alive:
            print("A", self.monster.name, "is here!")

        print("Exits:", ", ".join(self.exits))