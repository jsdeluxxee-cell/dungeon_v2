# My inventory
inventory = ["sword", "shield", "potion", "bow", "magic ring"]

print(inventory)
print(inventory[0])
print(inventory[1])
print(inventory[2])
print(inventory[3])


# Pick up a new item
inventory.append("magic ring")
print(inventory)

# Drop the shield
inventory.remove("shield")
print(inventory)

# Check how many items you have
print(f"You have {len(inventory)} items.")