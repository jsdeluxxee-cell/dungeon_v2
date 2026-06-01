from random import randint
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.alive = True

        self.current_room = None
        self.previous_room = None

    def take_damage(self, amount, attacker_name):
        self.health -= amount
        print(attacker_name, "hits you!")
        print("Your health is now", self.health)

        if self.health <= 0:
            print("You died!")
            self.alive = False

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"You healed for {amount} HP. Current HP: {self.health}")

    def pick_up(self, item):
        if isinstance(item, list):
            self.inventory.extend(item)
        else:
            self.inventory.append(item)
        print("You picked up:", item)


class Monster:
    def __init__(self, name, health, damage, attack_msg):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_msg = attack_msg
        self.alive = True

    def take_damage(self, amount):
        self.health -= amount
        print(f"You hit the {self.name} for {amount} damage!")

        if self.health <= 0:
            self.alive = False
            print(f"You defeated the {self.name}!")

    def attack(self, player):
        print(self.attack_msg)
        player.take_damage(self.damage, self.name)


class Moo(Monster):
    def __init__(self):
        super().__init__("mo'o", 60, 15, "The mo'o strikes from the water!")

    def attack(self, player):
        if "spear" not in player.inventory and "fishhook" not in player.inventory:
            print("The mo'o drags you underwater!")
            player.take_damage(self.damage + 10, self.name)
        else:
            super().attack(player)


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


class Kāmohoaliʻi(Monster):
    def __init__(self):
        super().__init__("Kāmohoaliʻi", 65, 20, "Kāmohoaliʻi bites from the deep!")


class Pele(Monster):
    def __init__(self):
        super().__init__("Pele", 40, 23, "Pele erupts in fire!")


MONSTER_CLASSES = {
    "Moo": Moo,
    "Nightmarcher": Nightmarcher,
    "Kāmohoaliʻi": Kāmohoaliʻi,
    "Pele": Pele
}


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


def load_dungeon(filename="dungeon.json"):
    with open(filename, "r", encoding="utf-8") as file:
        dungeon_data = json.load(file)

    loaded_rooms = {}

    for room_name, room_data in dungeon_data["rooms"].items():

        monster = None
        monster_type = room_data.get("monster_type")

        if monster_type in MONSTER_CLASSES:
            monster_class = MONSTER_CLASSES[monster_type]
            monster = monster_class()

        npc = None
        if "npc" in room_data:
            npc_data = room_data["npc"]
            npc = NPC(npc_data["name"], npc_data["dialogue"], npc_data["gift"])

        loaded_rooms[room_name] = Room(
            room_data["description"],
            room_data["exits"],
            room_data.get("item"),
            npc,
            monster
        )

    return loaded_rooms, dungeon_data["starting_room"]


rooms, starting_room = load_dungeon("ai_dungeon.json")

player = Player("Hero")

player.current_room = starting_room
player.previous_room = starting_room


def win_game():
    print("\nYOU WIN! YOU FOUND MAUI'S STONE!")
    player.alive = False


def show_room():
    room = rooms[player.current_room]
    room.describe()


def talk():
    room = rooms[player.current_room]
    if room.npc:
        room.npc.talk(player)
    else:
        print("No one here to talk to.")


def fight():
    room = rooms[player.current_room]
    monster = room.monster

    if not monster or not monster.alive:
        return

    print("\nA fight starts!")

    while monster.alive and player.alive:

        print("Your HP:", player.health)
        print(monster.name, "HP:", monster.health)

        action = input("attack, run, save: ").lower()

        if action == "save":
            continue

        if action == "run":
            player.current_room = player.previous_room
            return

        damage = 10
        if "fishhook" in player.inventory:
            damage += 15
        if "spear" in player.inventory:
            damage += 10

        monster.take_damage(damage)

        if not monster.alive:
            room.monster = None
            player.heal(15)
            break

        monster.attack(player)

        if player.health <= 0:
            player.alive = False
            return


def move(direction):
    room = rooms[player.current_room]

    for exit_name in room.exits:
        if direction.lower() == exit_name.lower():
            player.previous_room = player.current_room
            player.current_room = exit_name

            new_room = rooms[player.current_room]

            if new_room.monster and new_room.monster.alive:
                fight()

            return

    print("Can't go that way.")


def take():
    room = rooms[player.current_room]

    if room.item:
        player.pick_up(room.item)

        if room.item == "maui_stone":
            win_game()

        room.item = None
    else:
        print("Nothing here.")


def inventory():
    print("Inventory:", player.inventory)


def use(item_name):
    item_name = item_name.strip().lower()

    if item_name in player.inventory:

        if item_name == "canned_goods":
            player.heal(30)
            player.inventory.remove("canned_goods")
            print("You ate the canned goods.")
        else:
            print("You can't use that right now.")
    else:
        print("You don't have that item.")


while player.alive:
    show_room()
    action = input("\nWhat do you want to do? ").lower()

    if action == "quit":
        break
    elif action == "talk":
        talk()
    elif action == "take":
        take()
    elif action == "inventory":
        inventory()
    elif action.startswith("use "):
        use(action.replace("use ", ""))
    else:
        move(action)

print("Game Over")