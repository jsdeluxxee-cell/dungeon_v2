class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.alive = True

        self.current_room = None
        self.previous_room = None

    def take_damage(self, amount, attacker_name):
        self.health -= amount
        print(attacker_name, "hits you!")
        print("Your health is now", self.health)

        if self.health <= 0:
            print("You died!")
            self.alive = False

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"You healed for {amount} HP. Current HP: {self.health}")

    def pick_up(self, item):
        if isinstance(item, list):
            self.inventory.extend(item)
        else:
            self.inventory.append(item)
        print("You picked up:", item)