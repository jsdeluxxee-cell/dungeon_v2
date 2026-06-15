class Monster:
    def __init__(self, name, health, damage, attack_msg):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_msg = attack_msg
        self.alive = True

    def take_damage(self, amount):
        self.health -= amount
        print(f"You hit the {self.name} for {amount} damage!")

        if self.health <= 0:
            self.alive = False
            print(f"You defeated the {self.name}!")

    def attack(self, player):
        print(self.attack_msg)
        player.take_damage(self.damage, self.name)