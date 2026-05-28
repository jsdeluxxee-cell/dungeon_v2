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
        self.current_room = "beach"
        self.previous_room = "beach"

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

    def pick_up(self, item):
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

        if self.npc:
            print(self.npc.name, "is here.")

        if self.monster and self.monster.alive:
            print("A", self.monster.name, "is here!")

        print("Exits:", ", ".join(self.exits.keys()))


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


def save_game(player, rooms, filename="save.json"):
    save_data = {
        "player": {
            "name": player.name,
            "health": player.health,
            "current_room": player.current_room,
            "previous_room": player.previous_room,
            "inventory": player.inventory,
            "alive": player.alive
        },
        "rooms": {}
    }

    for room_name, room in rooms.items():
        save_data["rooms"][room_name] = {
            "item": room.item,
            "monster_alive": room.monster.alive if room.monster else None,
            "monster_health": room.monster.health if room.monster else None
        }

    with open(filename, "w") as file:
        json.dump(save_data, file, indent=2)

    print("Game saved!")


def load_dungeon(filename="dungeon.json"):
    with open(filename, "r") as file:
        dungeon_data = json.load(file)

    loaded_rooms = {}

    for room_name, room_data in dungeon_data["rooms"].items():

        monster = None
        if "monster_type" in room_data:
            monster_class = MONSTER_CLASSES[room_data["monster_type"]]
            monster = monster_class()

        npc = None
        if "npc" in room_data:
            npc_data = room_data["npc"]
            npc = NPC(npc_data["name"], npc_data["dialogue"], npc_data["gift"])

        loaded_rooms[room_name] = Room(
            room_data["description"],
            room_data["exits"],
            room_data["item"],
            npc,
            monster
        )

    return loaded_rooms, dungeon_data["starting_room"]


def load_game(rooms, filename="save.json"):
    try:
        with open(filename, "r") as file:
            save_data = json.load(file)

        player_data = save_data["player"]

        player = Player(player_data["name"])
        player.health = player_data["health"]
        player.current_room = player_data["current_room"]
        player.previous_room = player_data["previous_room"]
        player.inventory = player_data["inventory"]
        player.alive = player_data["alive"]

        for room_name, room_state in save_data["rooms"].items():
            rooms[room_name].item = room_state["item"]

            if rooms[room_name].monster and room_state["monster_alive"] is not None:
                rooms[room_name].monster.alive = room_state["monster_alive"]

            if rooms[room_name].monster and room_state["monster_health"] is not None:
                rooms[room_name].monster.health = room_state["monster_health"]

        return player

    except FileNotFoundError:
        logging.warning("No save file found.")
        return None

rooms, starting_room = load_dungeon()

player = Player("Hero")
player.current_room = starting_room
player.previous_room = starting_room


def win_game():
    print("\nYOU WIN! YOU FOUND MAUI'S STONE!")
    player.alive = False


def check_win():
    if "maui_stone" in player.inventory:
        win_game()


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
            save_game(player, rooms)
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

        if monster.alive:
            monster.attack(player)


def move(direction):
    room = rooms[player.current_room]

    if direction in room.exits:
        player.previous_room = player.current_room
        player.current_room = room.exits[direction]

        new_room = rooms[player.current_room]
        if new_room.monster and new_room.monster.alive:
            fight()
    else:
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
    if item_name == "canned_goods" and "canned_goods" in player.inventory:
        player.heal(30)
        player.inventory.remove("canned_goods")
        print("You ate the canned goods.")
    else:
        print("You can't use that.")


while True:
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
    elif action == "save":
        save_game(player, rooms)
    elif action == "load":
        loaded_player = load_game(rooms)

        if loaded_player:
            player = loaded_player
            check_win()

    elif action.startswith("use "):
        use(action.replace("use ", ""))
    else:
        move(action)

print("Game Over")