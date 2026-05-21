print("Welcome to the leaderboard!")
print("How many players do you want to add on the leaderboard? (max 5)")

num_players = min(int(input("Enter the number of players: ")), 5)

different_players = []

def add_player(player_number):
    player_name = input(f"Enter Player {player_number} name: ").title()
    player_score = int(input(f"Enter Player {player_number} score: "))
    player_level = int(input(f"Enter Player {player_number} level: "))
    player_kills = int(input(f"Enter Player {player_number} kills: "))

    return {
        "name": player_name,
        "score": player_score,
        "level": player_level,
        "kills": player_kills
    }

def display_leaderboard(players):
    print("\n=== LEADERBOARD ===")
    for i, player in enumerate(players):
        print(f"{i+1}. {player['name']} - {player['score'] + player['kills']} pts")

def show_stats(players):
    print(f"\nWinner: {players[0]['name'].title()}")
    print(f"Loser: {players[-1]['name'].title()}")

    total = sum(p["score"] + p["kills"] for p in players)
    print(f"Average score and kills was {total / len(players)}")

for i in range(num_players):
    different_players.append(add_player(i + 1))

different_players.sort(key=lambda x: x["score"] + x["kills"], reverse=True)

display_leaderboard(different_players)
show_stats(different_players)