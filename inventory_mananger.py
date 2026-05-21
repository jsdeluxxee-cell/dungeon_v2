# inventory manager
inventory = ["pickaxe", "revolver", "medkit", "sheild"]

print(inventory)
print(inventory[0])
print(inventory[1])
print(inventory[2])
print(inventory[3])

print("What item would you like to pick up?")
print("Would you like to pick up a shotgun, rifle, or grenade?")
new_item = input()
new_items = ['shotgun', 'rifle', 'grenade']


if new_item in new_items:
    inventory.append(new_item)
    print("You picked up a", new_item)
else:
    print("Invalid item.")


drop_item = input("What item would you like to drop? ")

if drop_item in inventory:
    inventory.remove(drop_item)
    print("You dropped a", drop_item)
    print("Updated inventory:", inventory)
else:
    print("That item is not in your inventory.")