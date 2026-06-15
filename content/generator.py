import json
from core.room import Room
from core.npc import NPC
from monsters.registry import MONSTER_CLASSES


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