def run_game(player, rooms, show_room, talk, take, inventory, use, move):
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