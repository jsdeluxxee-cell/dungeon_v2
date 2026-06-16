from content.generator import load_dungeon
from core.player import Player
from engine.engine import Engine

rooms, starting_room = load_dungeon("ai_dungeon.json")

player = Player("Hero")
player.current_room = starting_room
player.previous_room = starting_room

game = Engine(player, rooms)
game.run()