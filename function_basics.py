# Defining and using a function
def greet_player():
    print("Welcome to the game!")
    print("Good luck out there!")

#Now CALL the function
greet_player()

# A function that takes a parameter
def deal_damage(amount):
    print(f"You deal {amount} damage!")

    deal_damage(25)
    deal_damage(100)
    deal_damage(7)
