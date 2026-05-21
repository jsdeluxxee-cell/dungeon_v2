# Loot drop system for a game
loot = ["pickaxe", "rifle", "shotgun", "medkit", "shield"]

rare_items = ["rifle", "shotgun"]

print("You have defeated the enemy!")
print("loot dropped:\n")

rare_count = 0

for item in loot:
    if item in rare_items:
        print(f"{item} is RARE!")
        rare_count += 1
    else:
        print(f"You found: {item}")

print(f"\nYou picked up {len(loot)} items total!")
print(f"Rare items found: {rare_count}")
print("All loot added to your inventory!")