from colorama import Fore
from rpg_inventory import Inventory


class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.xp = 0
        self.gold = 20
        self.max_hp = 100
        self.hp = 100
        self.inventory = Inventory({"Potion": 2})
        self.skills = ["Fireball"]
        self.cooldowns = {}
        self.map_name = "forest"
        self.x = 1
        self.y = 1
        self.quest_data = {}
        self.game_won = False
        self.found_chests = []

    def gain_xp(self, amount):
        self.xp += amount
        print(Fore.GREEN + f"You gained {amount} XP.")
        self.check_level_up()

    def check_level_up(self):
        # Each level requires 30 times the current level in XP.
        while self.xp >= self.level * 30:
            self.xp -= self.level * 30
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            print(Fore.YELLOW + f"LEVEL UP! You reached level {self.level}.")
            if self.level == 2 and "Heal" not in self.skills:
                self.skills.append("Heal")
                print("You learned Heal!")
            elif self.level == 3 and "PowerStrike" not in self.skills:
                self.skills.append("PowerStrike")
                print("You learned PowerStrike!")

    def show_stats(self):
        print(f"\nCharacter: {self.username}")
        print(f"Level: {self.level} | XP: {self.xp}")
        print(f"HP: {self.hp}/{self.max_hp} | Gold: {self.gold}")
        print("Skills:", ", ".join(self.skills))
        print(f"Location: {self.map_name} ({self.x}, {self.y})")

    def to_dict(self):
        # This dictionary is the data TinyDB writes to the save file.
        return {
            "level": self.level,
            "xp": self.xp,
            "gold": self.gold,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "inventory": self.inventory.to_dict(),
            "skills": self.skills,
            "cooldowns": self.cooldowns,
            "map_name": self.map_name,
            "x": self.x,
            "y": self.y,
            "quest_data": self.quest_data,
            "game_won": self.game_won,
            "found_chests": self.found_chests,
        }

    @classmethod
    def from_dict(cls, username, data):
        # Rebuild a Player object using values loaded from TinyDB.
        player = cls(username)
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)
        player.gold = data.get("gold", 20)
        player.max_hp = data.get("max_hp", 100)
        player.hp = data.get("hp", player.max_hp)
        player.inventory = Inventory(data.get("inventory", {}))
        player.skills = data.get("skills", ["Fireball"])
        player.cooldowns = data.get("cooldowns", {})
        player.map_name = data.get("map_name", "forest")
        player.x = data.get("x", 1)
        player.y = data.get("y", 1)
        player.quest_data = data.get("quest_data", {})
        player.game_won = data.get("game_won", False)
        player.found_chests = data.get("found_chests", [])
        return player
