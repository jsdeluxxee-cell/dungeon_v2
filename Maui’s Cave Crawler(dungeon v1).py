rooms = {
    "beach": {
        "description": "You wake up on a quiet beach. A cave is to the north.",
        "exits": {"north": "cave_mouth"},
        "npc": None,
        "item": "torch",
        "monster": None
    },

    "cave_mouth": {
        "description": "A tunnel goes deeper. A kahuna sits by a fire.",
        "exits": {"south": "beach", "north": "pond"},
        "npc": {
            "name": "kahuna",
            "dialogue": "Take this fishhook. You will need it.",
            "gift": "fishhook",
            "given": False
        },
        "item": None,
        "monster": None
    },

    "pond": {
        "description": "A huge mo'o rises from the water!",
        "exits": {
            "south": "cave_mouth",
            "east": "abandoned_armory",
            "west": "abandoned_bakery"
        },
        "npc": None,
        "item": None,
        "monster": {
            "name": "mo'o",
            "health": 60,
            "damage": 15,
            "alive": True
        }
    },

    "abandoned_bakery": {
        "description": "An old bakery. You see canned goods.",
        "exits": {"east": "long_hallway"},
        "npc": None,
        "item": "canned_goods",
        "monster": None
    },

    "abandoned_armory": {
        "description": "An old armory. You see a spear.",
        "exits": {
            "west": "pond",
            "east": "long_hallway"
        },
        "npc": None,
        "item": "spear",
        "monster": None
    },

    "long_hallway": {
        "description": "A hallway leads to a strange door.",
        "exits": {
            "west": "abandoned_armory",
            "north": "abandoned_bakery",
            "door": "mysterious_door"
        },
        "npc": None,
        "item": None,
        "monster": {
            "name": "Nightmarcher",
            "health": 70,
            "damage": 19,
            "alive": True
        }
    },

    "mysterious_door": {
        "description": "A locked glowing door hums with energy(need fishhook to enter). as you enter one by one lights flick on until you reach the Maui’s stone you take it and win",
        "exits": {"back": "long_hallway"},
        "npc": None,
        "item": "maui_stone",
        "monster": None
    }
}


player = {
    "current_room": "beach",
    "previous_room": "beach",
    "inventory": [],
    "health": 100,
    "alive": True
}


#-------------DOOR CHECK-----------------
def check_fishhook():
    if "fishhook" in player["inventory"]:
        print("You Have the fishhook so you can enter mysterious door")
        return True
    return False


#-------------WIN CHECK-----------------
def check_win():
    if "maui_stone" in player["inventory"]:
        print("You found Maui's stone and won the game!")
        player["alive"] = False
        return True
    return False

# ---------------- ROOM ----------------
def show_room():
    room = rooms[player["current_room"]]

    print("\n" + room["description"])

    if room["item"]:
        print("You see:", room["item"])

    if room["npc"]:
        print(room["npc"]["name"], "is here.")

    if room["monster"] and room["monster"]["alive"]:
        print("A", room["monster"]["name"], "is here!")

    print("Exits:", ", ".join(room["exits"].keys()))


# ---------------- TALK ----------------
def talk():
    room = rooms[player["current_room"]]

    if not room["npc"]:
        print("No one here to talk to.")
        return

    npc = room["npc"]
    print(npc["dialogue"])

    if not npc["given"]:
        player["inventory"].append(npc["gift"])
        npc["given"] = True
        print("You got:", npc["gift"])


# ---------------- FIGHT ----------------
def fight():
    room = rooms[player["current_room"]]
    monster = room["monster"]

    if not monster or not monster["alive"]:
        return

    print("\nA fight starts!")

    while monster["alive"] and player["alive"]:

        print("Your HP:", player["health"])
        print(monster["name"], "HP:", monster["health"])

        action = input("attack or run: ")

        if action == "run":
            print("You ran away!")
            player["current_room"] = player["previous_room"]
            return

        damage = 10

        if "fishhook" in player["inventory"]:
            damage += 15

        if "spear" in player["inventory"]:
            damage += 10

        monster["health"] -= damage
        print("You deal", damage)

        if monster["health"] <= 0:
            print("You defeated the monster!")
            monster["alive"] = False
            break

        player["health"] -= monster["damage"]
        print("Monster hits you!")

        if player["health"] <= 0:
            print("You died!")
            player["alive"] = False
            break


# ---------------- MOVE ----------------
def move(direction):
    room = rooms[player["current_room"]]

    if direction in room["exits"]:

        player["previous_room"] = player["current_room"]

        player["current_room"] = room["exits"][direction]

        new_room = rooms[player["current_room"]]

        if new_room["monster"] and new_room["monster"]["alive"]:
            fight()

    else:
        print("Can't go that way.")


# ---------------- TAKE ----------------
def take():
    room = rooms[player["current_room"]]

    if room["item"]:
        print("You picked up:", room["item"])
        player["inventory"].append(room["item"])
        room["item"] = None

        check_win()

    else:
        print("Nothing here.")


# ---------------- INVENTORY ----------------
def inventory():
    print("Inventory:", player["inventory"])


# ---------------- USE ITEM ----------------
def use(item_name):

    if item_name == "canned_goods":

        if "canned_goods" in player["inventory"]:

            player["health"] += 30

            if player["health"] > 100:
                player["health"] = 100

            player["inventory"].remove("canned_goods")

            print("You ate the canned goods.")
            print("Health:", player["health"])

        else:
            print("You don't have that item.")

    else:
        print("You can't use that.")


# ---------------- GAME LOOP ----------------
while player["alive"]:

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
        item = action.replace("use ", "")
        use(item)

    else:
        move(action)

print("Game Over")
