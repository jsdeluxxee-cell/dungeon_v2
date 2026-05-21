#guessing_game
from random import randint

secret_number = randint(1, 20)
guesses = float("inf")

print("I am thinking of a number between 1 and 20.")
print("You have infinite guesses to find the number.")

hint = input("Would you like a hint? (yes/no): ")
if hint.lower() == "yes":
    if secret_number % 2 == 0:
        print("The number is even.")
    else:
        print("The number is odd.")
    if secret_number > 10:
        print("The number is greater than 10.")
    else:
        print("The number is 10 or less.")
guess_counter = 0

while guesses > 0:
    guess = int(input("Enter your guess: "))
    guess_counter += 1
    if guess == secret_number:
        print("Congratulations! You guessed the number!")
        print("It took you", guess_counter, "guesses to find the number.")
        break
    if guesses != float("inf"):
        guesses -= 1
    print("You took", guess_counter, "guesses.")
    if guess > secret_number:
        print("Your guess is too high.")
    elif guess < secret_number:
        print("Your guess is too low.")
    if guesses > 0:
        print("Try again!")
        if guesses == float("inf"):
            print("You have infinite guesses left.")
        else:
            print("You have", guesses, "guesses left.")

       

