import random
import json

PLACE_TYPES = {"Cavern", "Hollow", "Chamber"}
CONNECTORS = {"of the", "of Forgotten"}
SUBJECTS = {"Kahuna", "Bones", "Pele"}

MONSTER_POOL = ["Moo", "Nightmarcher", "Kāmohoaliʻi", "Pele"]

used_names = set()


def generate_room_name():
    place_type = random.choice(list(PLACE_TYPES))
    connector = random.choice(list(CONNECTORS))
    subject = random.choice(list(SUBJECTS))

    full_name = f"{place_type} {connector} {subject}"
    return full_name, place_type


def get_unique_name():
    while True:
        full_name, place_type = generate_room_name()
        if full_name not in used_names:
            used_names.add(full_name)
            return full_name, place_type


def generate_description(place_type):
    return f"You are inside a {place_type.lower()}. The air feels strange."


def generate_dungeon(num_rooms=5):
    rooms = {}
    room_info = []

    # generate names
    for i in range(num_rooms):
        room_name, place_type = get_unique_name()
        room_info.append((room_name, place_type))

    # build rooms
    for i, (room_name, place_type) in enumerate(room_info):

        exits = {}

        if i > 0:
            exits["west"] = room_info[i - 1][0]

        if i < num_rooms - 1:
            exits["east"] = room_info[i + 1][0]

        # RULES
        if i == 0:
            monster = None
            item = None

        elif i == num_rooms - 1:
            monster = None
            item = "maui_stone"

        else:
            monster = random.choice(MONSTER_POOL)
            item = None

        rooms[room_name] = {
            "description": generate_description(place_type),
            "exits": exits,
            "item": item,
            "monster_type": monster
        }

    return rooms


dungeon = generate_dungeon()

with open("dungeon.json", "w") as f:
    json.dump({
        "starting_room": list(dungeon.keys())[0],
        "rooms": dungeon
    }, f, indent=2)

print("Dungeon saved to dungeon.json")