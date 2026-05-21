# Combat outcome check
enemy_health =int(input("Enter enemy health: "))
damage_dealt =int(input("Enter damage dealt: "))

remaining_health = enemy_health - damage_dealt
if remaining_health <= 0:
    print("Enemy defeated! You win!")
elif remaining_health <= 20:
    print(f"enemy is crititcal! Only {remaining_health} HP left!")

else:
    print(f"Enemy still alive with {remaining_health} HP keep fighting!")

enemy_difficulty = int(input("Enter enemy difficulty (1-10): "))
if enemy_difficulty >= 8:
    print("Legandery Loot drop!")
elif enemy_difficulty >= 5:
    print("Rare Loot drop!")
else:
    print("Common Loot drop!")