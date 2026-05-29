import json
import random

TEXTURES = {
    "rough stone walls",
    "damp cave surfaces",
    "cracked lava rock"
}

SCENTS = {
    "sulfur hangs in the air",
    "wet earth fills the room",
    "saltwater drifts through the chamber"
}

MOODS = {
    "an eerie calm",
    "a strange stillness",
    "an uneasy silence"
}

SOUNDS = {
    "water drips in the distance",
    "wind whistles through cracks",
    "stones grind softly nearby"
}

LIGHT_STATES = {
    "Torchlight flickers",
    "Dim blue light glows",
    "Shadows dance across the walls"
}

FEATURES = {
    "a stone altar",
    "broken statues",
    "ancient carvings"
}

FEATURE_ALT = {
    "a collapsed pillar",
    "a ring of volcanic stone",
    "a weathered shrine"
}

CARVINGS = {
    "spiral markings",
    "ancient Hawaiian symbols",
    "weathered battle scenes"
}

STARTING_TEMPLATES = {
    "{light}. {feature} stands near the entrance, and {sound}."
}

MIDDLE_TEMPLATES = {
    "{light} across the {place_type}. {texture} surrounds you while {scent}.",
    "{sound}. {feature} rests beneath {carving}, and {mood} fills the chamber."
}

FINAL_TEMPLATES = {
    "{light}. The air feels heavy inside the {place_type}, and {feature_alt} sits beneath {carving}."
}

MONSTER_PRESENCE = {
    "A {monster} emerges from the shadows.",
    "You suddenly spot a {monster} watching you carefully."
}

MAUI_STONE_PRESENCE = {
    "A glowing Maui Stone rests at the center of the room.",
    "The legendary Maui Stone radiates power before you."
}

PLACE_TYPES = {
    "Cave",
    "Temple",
    "Ruins",
    "Volcanic Chamber"
}

CONNECTORS = {
    "of",
    "beneath",
    "near",
    "beyond",
    "under"
}

SUBJECTS = {
    "Fire",
    "Bones",
    "Storms",
    "Whispers",
    "Ancients",
    "Tides",
    "Shadows",
    "the Volcano"
}

MONSTER_POOL = {
    "Moo",
    "Nightmarcher",
    "Kāmohoaliʻi",
    "Pele"
}

ITEM_POOL = {
    "health_potion",
    "lava_charm",
    "ancient_coin",
    "torch"
}

used_names = set()


def generate_room_name():
    while True:
        place_type = random.choice(tuple(PLACE_TYPES))
        room_name = (
            f"{place_type} "
            f"{random.choice(tuple(CONNECTORS))} "
            f"{random.choice(tuple(SUBJECTS))}"
        )
        if room_name not in used_names:
            used_names.add(room_name)
            return (room_name, place_type)


def generate_room_description(place_type, room_position, total_rooms, monster=None):
    if room_position == 0:
        templates = STARTING_TEMPLATES
    elif room_position == total_rooms - 1:
        templates = FINAL_TEMPLATES
    else:
        templates = MIDDLE_TEMPLATES

    template = random.choice(tuple(templates))

    description = template.format(
        place_type=place_type.lower(),
        texture=random.choice(tuple(TEXTURES)),
        scent=random.choice(tuple(SCENTS)),
        mood=random.choice(tuple(MOODS)),
        sound=random.choice(tuple(SOUNDS)),
        light=random.choice(tuple(LIGHT_STATES)),
        feature=random.choice(tuple(FEATURES)),
        feature_alt=random.choice(tuple(FEATURE_ALT)),
        carving=random.choice(tuple(CARVINGS))
    )

    if monster is not None:
        monster_text = random.choice(tuple(MONSTER_PRESENCE))
        description += " " + monster_text.format(monster=monster)

    if room_position == total_rooms - 1:
        description += " " + random.choice(tuple(MAUI_STONE_PRESENCE))

    return description


def generate_dungeon(total_rooms):
    dungeon = []

    for room_position in range(total_rooms):

        room_name, place_type = generate_room_name()

        if room_position == total_rooms - 1:
            room_name = "Temple of Fire"

        if room_position == 0:
            monster = None
        elif room_position == total_rooms - 1:
            monster = "Pele"
        else:
            monster = random.choice(tuple(MONSTER_POOL))

        description = generate_room_description(
            place_type,
            room_position,
            total_rooms,
            monster
        )

        exits = []

        if room_position > 0:
            exits.append(dungeon[room_position - 1]["name"])

        # FIXED ITEM LOGIC: room 1 now gives both healing and weapon
        if room_position == 1:
            item = ["canned_goods", "fishhook"]
        elif room_position == total_rooms - 1:
            item = "maui_stone"
        else:
            item = None

        room = {
            "name": room_name,
            "type": place_type,
            "description": description,
            "monster_type": monster,
            "item": item,
            "exits": exits
        }

        dungeon.append(room)

        if room_position > 0:
            dungeon[room_position - 1]["exits"].append(room_name)

    return dungeon


dungeon_data = {
    "starting_room": None,
    "rooms": {}
}

dungeon_rooms = generate_dungeon(5)

dungeon_data["starting_room"] = dungeon_rooms[0]["name"]

for room in dungeon_rooms:
    dungeon_data["rooms"][room["name"]] = {
        "type": room["type"],
        "description": room["description"],
        "monster_type": room["monster_type"],
        "item": dungeon_rooms[dungeon_rooms.index(room)]["item"],
        "exits": room["exits"]
    }

with open("dungeon.json", "w") as file:
    json.dump(dungeon_data, file, indent=4)

print("Dungeon generated successfully!")