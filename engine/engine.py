from content.generator import load_dungeon
from core.player import Player


class Engine:
    def __init__(self):
        self.rooms, self.starting_room = load_dungeon("content/ai_dungeon.json")

        self.player = Player("Hero")
        self.player.current_room = self.starting_room
        self.player.previous_room = self.starting_room

    def run(self):
        while self.player.alive:
            self.show_room()

            action = input("\nWhat do you want to do? ").lower()

            if action == "quit":
                break
            elif action == "talk":
                self.talk()
            elif action == "take":
                self.take()
            elif action == "inventory":
                self.inventory()
            elif action.startswith("use "):
                self.use(action.replace("use ", ""))
            else:
                self.move(action)

        print("Game Over")

    def show_room(self):
        room = self.rooms[self.player.current_room]

        print("\n" + room.description)

        if room.exits:
            print("\nExits:")
            for exit_name in room.exits:
                print("-", exit_name)

        if room.item:
            print(f"You see a {room.item} here.")

        if room.npc:
            print("Someone is here you can talk to.")

        if room.monster and room.monster.alive:
            print("A wild", room.monster.name, "is here!")

    def talk(self):
        room = self.rooms[self.player.current_room]

        if room.npc:
            room.npc.talk(self.player)
        else:
            print("No one here to talk to.")

    def take(self):
        room = self.rooms[self.player.current_room]

        if not room.item:
            print("Nothing here.")
            return

        item = room.item

        self.player.pick_up(item)
        print(f"You took the {item}.")

        if item == "maui_stone":
            self.win_game()

        room.item = None

    def inventory(self):
        print("Inventory:", self.player.inventory)

    def use(self, item_name):
        item_name = item_name.strip().lower()

        if item_name not in self.player.inventory:
            print("You don't have that item.")
            return

        if item_name == "canned_goods":
            self.player.heal(30)
            self.player.inventory.remove("canned_goods")
            print("You used canned goods and healed 30 HP.")
        else:
            print(f"You used the {item_name}, but nothing happened.")

    def move(self, direction):
        room = self.rooms[self.player.current_room]

        for exit_name in room.exits:
            if direction.lower() == exit_name.lower():
                self.player.previous_room = self.player.current_room
                self.player.current_room = exit_name

                new_room = self.rooms[self.player.current_room]

                if new_room.monster and new_room.monster.alive:
                    self.fight()

                return

        print("Can't go that way.")

    def fight(self):
        room = self.rooms[self.player.current_room]
        monster = room.monster

        if not monster or not monster.alive:
            return

        print("\nA fight starts!")

        while monster.alive and self.player.alive:

            print("Your HP:", self.player.health)
            print(monster.name, "HP:", monster.health)

            action = input("attack, run, save: ").lower()

            if action == "save":
                continue

            if action == "run":
                self.player.current_room = self.player.previous_room
                return

            damage = 10

            if "fishhook" in self.player.inventory:
                damage += 15
            if "spear" in self.player.inventory:
                damage += 10

            monster.take_damage(damage)

            if not monster.alive:
                room.monster = None
                self.player.heal(15)
                print("You defeated the monster!")
                break

            monster.attack(self.player)

            if self.player.health <= 0:
                self.player.alive = False
                print("You died...")
                return

    def win_game(self):
        print("\nYOU WIN! YOU FOUND MAUI'S STONE!")
        self.player.alive = False