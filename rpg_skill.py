class Skill:
    # Parent class for skills. Child classes define their own effects.
    def __init__(self, name, cooldown):
        self.name = name
        self.cooldown = cooldown

    def use(self, player, monster):
        pass


class Fireball(Skill):
    def __init__(self):
        super().__init__("Fireball", 2)

    def use(self, player, monster):
        damage = 22
        monster.hp -= damage
        print(f"Fireball deals {damage} damage!")
        return self.cooldown


class Heal(Skill):
    def __init__(self):
        super().__init__("Heal", 3)

    def use(self, player, monster):
        healing = 30
        actual_healing = min(healing, player.max_hp - player.hp)
        player.hp += actual_healing
        print(f"Heal restores {actual_healing} HP!")
        return self.cooldown


class PowerStrike(Skill):
    def __init__(self):
        super().__init__("PowerStrike", 3)

    def use(self, player, monster):
        damage = 35
        monster.hp -= damage
        print(f"PowerStrike deals {damage} damage!")
        return self.cooldown


def get_skill(skill_name):
    skill_types = {
        "Fireball": Fireball,
        "Heal": Heal,
        "PowerStrike": PowerStrike,
    }
    return skill_types[skill_name]()
