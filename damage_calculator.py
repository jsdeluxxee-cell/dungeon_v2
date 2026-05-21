# Trying to do math with input
weapon_damage = int(input("Enter your weapon damage: "))
crit_bonus = int(input("Enter your crit bonus: "))
enemy_armor = int(input("enter enemy armor: "))
enemy_health = int(input("enter enemy health: "))

total = (weapon_damage + crit_bonus) - enemy_armor
remaining_health = enemy_health - total

print(f"total damage: {total}")
print(f"remaining health: {remaining_health}")
