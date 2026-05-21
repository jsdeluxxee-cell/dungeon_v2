# combat_functions.py

def attack(damage):
    print(f"You attack for {damage} damage!")

def heal(amount):
    print(f"You heal for {amount} health!")

def calculate_total_damage(weapon, crit, multiplier):
    total = (weapon + crit) * multiplier
    return total

# enemy setup
enemy_health = 100

print("You attack the enemy!")

result = calculate_total_damage(40, 10, 2)
attack(result)

enemy_health -= result

print(f"Enemy health: {enemy_health}")

if enemy_health <= 0:
    print("Enemy defeated!")
else:
    print("Enemy is still alive!")