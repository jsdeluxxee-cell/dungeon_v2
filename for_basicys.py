# Looping through enemies
enemies = ["zombie", "skeleton", "creeper", "spider"]

for enemy in enemies:
    print(f"A {enemy} has appeared!")

# Apply posion damage to each enemy
enemy_count = 0
for enemy in enemies:
    enemy_count += 1
    print(f"Enemy#{enemy_count}: {enemy} takes 5 poison damage. ")