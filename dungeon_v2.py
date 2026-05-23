from random import randint


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


class Pueo(Monster):
    def __init__(self):
        super().__init__("Pueo", 40, 12, "The Pueo swoops in!")

    def take_damage(self, amount):
        if randint(1, 2) == 1:
            print("The Pueo dodged your attack!")
            return
        super().take_damage(amount)


class Kahuli(Monster):
    def __init__(self):
        super().__init__("kahuli", 80, 15, "The kahuli attacks!")


class Kāmohoaliʻi(Monster):
    def __init__(self):
        super().__init__("Kāmohoaliʻi", 65, 20, "Kāmohoaliʻi bites from the deep!")


class Pele(Monster):
    def __init__(self):
        super().__init__("Pele", 40, 23, "Pele erupts in fire!")


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


import json

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



def load_game(filename="save.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        name = lines[0].strip()
        health = int(lines[1].strip())
        current_room = lines[2].strip()
        previous_room = lines[3].strip()
        inventory_string = lines[4].strip()
        alive = lines[5].strip() == "True"

        player = Player(name)
        player.health = health
        player.current_room = current_room
        player.previous_room = previous_room
        player.alive = alive

        if inventory_string:
            player.inventory = inventory_string.split(",")
        else:
            player.inventory = []

        for line in lines[6:]:
            line = line.strip()

            if not line:
                continue

            room_name, item_value, monster_alive, monster_health = line.split("|")

            rooms[room_name].item = None if item_value == "None" else item_value

            if rooms[room_name].monster:
                rooms[room_name].monster.alive = (monster_alive == "True")

                if monster_health != "None":
                    rooms[room_name].monster.health = int(monster_health)

        print("Game loaded!")
        return player

    except FileNotFoundError:
        print("No save file found.")
        return None


rooms = {
    "beach": Room(
        "You wake up on a quiet beach. A cave is to the north.",
        {"north": "cave_mouth"},
        item="torch"
    ),
    "cave_mouth": Room(
        "A tunnel goes deeper. A kahuna sits by a fire.",
        {"south": "beach", "north": "pond"},
        npc=NPC("kahuna", "Take this fishhook. You will need it.", "fishhook")
    ),
    "pond": Room(
        "A huge mo'o rises from the water!",
        {"south": "cave_mouth", "east": "abandoned_armory", "west": "abandoned_bakery"},
        monster=Moo()
    ),
    "abandoned_bakery": Room(
        "An old bakery. Heat fills the air...",
        {"east": "long_hallway"},
        item="canned_goods",
        monster=Pele()
    ),
    "abandoned_armory": Room(
        "An old armory filled with broken weapons.",
        {"west": "pond", "east": "long_hallway"},
        item="spear",
        monster=Kāmohoaliʻi()
    ),
    "long_hallway": Room(
        "A dark hallway stretches ahead.",
        {"west": "abandoned_armory", "north": "abandoned_bakery", "door": "mysterious_door"},
        monster=Nightmarcher()
    ),
    "mysterious_door": Room(
        "A glowing door hums with energy...",
        {"back": "long_hallway"},
        item="maui_stone"
    )
}


player = Player("Hero")


def win_game():
    print("\nYOU WIN! YOU FOUND MAUI'S STONE!")
    player.alive = False


def show_room():
    room = rooms[player.current_room]
    room.describe()


def talk():
    room = rooms[player.current_room]

    if not room.npc:
        print("No one here to talk to.")
        return

    room.npc.talk(player)


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
            save_game(player)
            continue

        if action == "run":
            print("You ran away!")
            player.current_room = player.previous_room
            return

        damage = 10

        if "fishhook" in player.inventory:
            damage += 15

        if "spear" in player.inventory:
            damage += 10

        monster.take_damage(damage)

        if not monster.alive:
            break

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
    if item_name == "canned_goods":
        if "canned_goods" in player.inventory:
            player.heal(30)
            player.inventory.remove("canned_goods")
            print("You ate the canned goods.")
        else:
            print("You don't have that item.")
    else:
        print("You can't use that.")


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
    elif action == "save":
        save_game(player)
    elif action == "load":
        loaded = load_game()
        if loaded is not None:
            player = loaded
    elif action.startswith("use "):
        use(action.replace("use ", ""))
    else:
        move(action)

print("Game Over")