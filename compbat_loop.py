enemy_health = 100

while enemy_health > 0:
    attack_damage = int(input("Enter your attack damage: "))
    enemy_health = enemy_health - attack_damage
    print(f"Enemy's remaining health: {enemy_health}")

print("Enemy defeated!")