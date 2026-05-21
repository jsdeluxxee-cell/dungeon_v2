class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.alive = True
    
    def say_hello(self):
        print(f"Hi, I'm {self.name}!")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} took {amount} damage! Health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} has died!")
    
    def show_status(self):
        print("Name:", self.name)
        print("Health:", self.health)
        print("Inventory:", self.inventory)
        print("Alive:", self.alive)
    
    def pick_up(self, item):
        self.inventory.append(item)
        print(f"{self.name} picked up {item}")
    
    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{self.name} dropped {item}")
        else:
            print(f"{self.name} doesn't have {item}")
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        print(f"{self.name} healed {amount} HP! Health: {self.health}/{self.max_health}")


braylin = Player("Braylin")
braylin.take_damage(30)
braylin.show_status()

kainoa = Player("Kainoa")
kainoa.show_status()

kainoa.pick_up("torch")
kainoa.pick_up("spear")
kainoa.take_damage(20)
kainoa.heal(15)
kainoa.take_damage(200)
kainoa.drop("banana")
kainoa.show_status()

braylin = Player("Braylin")
braylin.take_damage(30)
braylin.show_status()