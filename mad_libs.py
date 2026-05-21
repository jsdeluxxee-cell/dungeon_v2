# Mad Lib Generator

def tell_story(noun, verb, adjective, a_number, a_game, adverb, place, year, name):
    print("Welcome to the Mad Libs Generator!")
    print("Here is your Mad libs story:")
    print(f"Once upon a time in {year} there was a person named {name}. ")
    print(f"There was a {adjective} {noun} who loved to play {a_game}")
    print(f"One day, the {noun} decided to play {a_game} and {adverb} won the game with a score of {a_number}.")
    print(f"The {noun} was so happy that it decided to {verb} all day with his friend {name} at {place}.")
    print("----- STORY COMPLETE -----")


def mad_libs():
    noun = input("Enter a noun: ")
    verb = input("Enter a verb: ")
    adjective = input("Enter an adjective: ")
    a_number = input("Enter a number: ")
    a_game = input("Enter a game: ")
    adverb = input("Enter an adverb: ")
    place = input("Enter a place: ")
    year = input("Enter a year: ")
    name = input("Enter a name: ").title()

    tell_story(noun, verb, adjective, a_number, a_game, adverb, place, year, name)

mad_libs()