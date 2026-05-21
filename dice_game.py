from random import randint

def roll_dice(num_dice, sides):
    rolls = []

    for i in range(num_dice):
        roll = randint(1, sides)
        rolls.append(roll)

    return rolls


def display_results(rolls, sides):
    print("\nResults:")
    
    for roll in rolls:
        print(f"You rolled: {roll}")

    print("\nTotal:", sum(rolls))
    print("Highest roll:", max(rolls))
    print("Lowest roll:", min(rolls))

    # optional flex features (what makes it stand out)
    if max(rolls) == sides:
        print("CRITICAL HIT!")

    if all(r == 1 for r in rolls):
        print("SNAKE EYES!")


print("Welcome to the Dice Roller Game!")

num_dice = int(input("How many dice do you want to roll? "))
sides = int(input("How many sides does each die have? "))

results = roll_dice(num_dice, sides)
display_results(results, sides)