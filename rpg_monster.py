import random


class Monster:
    # Parent class: every monster has these shared properties and behavior.
    def __init__(self, name, hp, damage, xp, gold, drop):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.xp = xp
        self.gold = gold
        self.drop = drop

    def attack(self):
        return random.randint(max(1, self.damage - 3), self.damage + 3)


class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 35, 10, 12, 8, "Herb")


class Slime(Monster):
    def __init__(self):
        super().__init__("Slime", 25, 7, 8, 5, "Herb")


class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", 45, 13, 15, 10, "Potion")


class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", 55, 15, 18, 12, "Herb")


class DarkKnight(Monster):
    def __init__(self):
        super().__init__("Dark Knight", 70, 18, 22, 18, "Potion")


class Boss(Monster):
    def __init__(self):
        super().__init__("Crystal Guardian", 150, 22, 100, 100, "Crystal Shard")


def create_random_monster():
    # These are the five normal monster types. The boss is separate.
    monster_type = random.choice([Goblin, Slime, Wolf, Skeleton, DarkKnight])
    return monster_type()
