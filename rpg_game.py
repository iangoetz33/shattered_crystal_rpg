import random
from colorama import Fore, Style, init

from rpg_auth import register_or_login
from rpg_database import save_player
from rpg_player import Player
from rpg_map import GameMap
from rpg_monster import create_random_monster, Boss
from rpg_combat import battle
from rpg_npc import NPCS
from rpg_quest import QuestManager
from rpg_shop import visit_shop
from rpg_inventory import show_inventory, use_item

init(autoreset=True)


class Game:
    def __init__(self):
        self.player = None
        self.quests = None
        self.game_map = None
        self.steps_since_battle = 0

    def start(self):
        print(Fore.CYAN + Style.BRIGHT + "\nTHE SHATTERED CRYSTAL")
        print("Long ago, a magical crystal protected the kingdom from darkness.")
        print("One night, the crystal was stolen. Monsters now roam the land.")
        print("Find the Elder, complete the quests, and defeat the Crystal Guardian.\n")

        username, saved_data = register_or_login()
        if saved_data:
            self.player = Player.from_dict(username, saved_data)
            print(Fore.GREEN + "Your saved adventure has been restored.")
        else:
            self.player = Player(username)
            print("Your adventure begins in the forest.")

        self.quests = QuestManager.from_dict(self.player.quest_data)
        self.game_map = GameMap(self.player.map_name, self.player.x, self.player.y)
        self.game_loop()

    def game_loop(self):
        while self.player.hp > 0 and not self.player.game_won:
            self.game_map.draw()
            self.show_status()
            print("\nCommands: W/A/S/D move | talk | shop | inventory | use")
            print("          stats | quest | save | help | quit")
            command = input("> ").strip().lower()

            if command in ("w", "a", "s", "d"):
                self.move_player(command)
            elif command == "talk":
                self.talk()
            elif command == "shop":
                self.open_shop()
            elif command == "inventory":
                show_inventory(self.player)
            elif command == "use":
                use_item(self.player)
            elif command == "stats":
                self.player.show_stats()
            elif command == "quest":
                self.quests.show()
            elif command == "save":
                self.save()
            elif command == "help":
                self.show_help()
            elif command == "quit":
                self.save()
                print("Progress saved. Goodbye!")
                return
            else:
                print(Fore.YELLOW + "Unknown command. Type help to see the commands.")

        if self.player.hp <= 0:
            print(Fore.RED + "\nYou were defeated. Your progress has been saved.")
            self.save()
        elif self.player.game_won:
            print(Fore.YELLOW + Style.BRIGHT + "\nYOU DEFEATED THE CRYSTAL GUARDIAN!")
            print("The crystal's light returns. The kingdom is safe. YOU WIN!")
            self.save()

    def show_status(self):
        print(
            Fore.GREEN + f"\n{self.player.username} | Level {self.player.level} | "
            f"HP {self.player.hp}/{self.player.max_hp} | XP {self.player.xp} | "
            f"Gold {self.player.gold}"
        )

    def move_player(self, direction):
        dx = {"a": -1, "d": 1}.get(direction, 0)
        dy = {"w": -1, "s": 1}.get(direction, 0)
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if not self.game_map.can_move(new_x, new_y):
            print(Fore.YELLOW + "You cannot move there. A wall is blocking the way.")
            return

        self.player.x, self.player.y = new_x, new_y
        self.check_location()

        # The portal is at (7, 5) in the forest.
        if self.player.map_name == "forest" and (new_x, new_y) == (7, 5):
            if self.quests.main_stage < 3:
                print(Fore.YELLOW + "The castle portal is sealed. Finish the Elder's task first.")
                self.player.x, self.player.y = 6, 5
            else:
                self.player.map_name = "castle"
                self.player.x, self.player.y = 1, 1
                print(Fore.CYAN + "You step through the portal and enter the castle.")

        # The boss chamber is at (8, 6) in the castle.
        elif self.player.map_name == "castle" and (new_x, new_y) == (8, 6):
            if self.quests.main_stage < 3:
                print(Fore.YELLOW + "The boss chamber is sealed.")
            else:
                self.start_boss_battle()

        self.game_map = GameMap(self.player.map_name, self.player.x, self.player.y)

        if self.player.map_name in ("forest", "castle"):
            self.steps_since_battle += 1
            if self.steps_since_battle >= 4:
                self.steps_since_battle = 0
                if random.random() < 0.55:
                    monster = create_random_monster()
                    print(Fore.RED + f"\nA wild {monster.name} appears!")
                    if battle(self.player, monster):
                        self.quests.record_monster_defeat()
                        self.player.check_level_up()
                        self.player.quest_data = self.quests.to_dict()

    def check_location(self):
        chest = f"{self.player.map_name}_{self.player.x}_{self.player.y}"
        if chest in ("forest_3_2", "castle_3_2") and chest not in self.player.found_chests:
            self.player.found_chests.append(chest)
            if chest == "forest_3_2":
                self.player.inventory.add("Herb", 1)
                self.player.inventory.add("Potion", 1)
                print(Fore.CYAN + "You opened a forest chest: 1 Herb and 1 Potion.")
            else:
                self.player.inventory.add("Potion", 1)
                print(Fore.CYAN + "You opened a castle chest: 1 Potion.")

    def talk(self):
        nearby = []
        for npc in NPCS:
            if npc.map_name == self.player.map_name:
                distance = abs(npc.x - self.player.x) + abs(npc.y - self.player.y)
                if distance <= 1:
                    nearby.append(npc)

        if not nearby:
            print("There is nobody close enough to talk to.")
            return

        # If two NPCs are nearby, talk to the closest one.
        npc = min(
            nearby,
            key=lambda person: abs(person.x - self.player.x) + abs(person.y - self.player.y)
        )
        print(Fore.CYAN + f"\n{npc.name}: {npc.dialogue}")

        if npc.name == "Elder":
            if self.quests.main_stage == 0:
                self.quests.main_stage = 1
                print(Fore.GREEN + "Main quest started: defeat 3 monsters.")
            elif self.quests.main_stage == 2:
                self.quests.main_stage = 3
                print(Fore.GREEN + "The Elder gives you the key. The castle portal is now open.")
            elif self.quests.main_stage == 3:
                print("The Crystal Guardian waits in the castle. Finish this!")
            elif self.quests.main_stage == 4:
                print("You have already saved the kingdom. Thank you, hero.")

        elif npc.name == "Guard":
            quest = self.quests.side_quests["monster_hunt"]
            if not quest["accepted"]:
                self.quests.accept_side_quest("monster_hunt")
                print("Side quest accepted: defeat 2 monsters.")
            elif quest["complete"] and not quest["rewarded"]:
                quest["rewarded"] = True
                self.player.gold += 25
                self.player.gain_xp(20)
                self.player.inventory.add("Potion", 1)
                print(Fore.GREEN + "Quest reward: 25 gold, 20 XP, and 1 Potion.")
            elif quest["complete"]:
                print("Thanks again for helping the guards.")
            else:
                print(f"Monster Hunt progress: {quest['progress']}/2 monsters.")

        elif npc.name == "Healer":
            quest = self.quests.side_quests["herb_search"]
            if not quest["accepted"]:
                self.quests.accept_side_quest("herb_search")
                print("Side quest accepted: bring the Healer 2 Herbs.")
            elif not quest["complete"]:
                if self.player.inventory.items.get("Herb", 0) >= 2:
                    self.player.inventory.remove("Herb", 2)
                    quest["complete"] = True
                    self.player.gold += 20
                    self.player.gain_xp(25)
                    self.player.inventory.add("Potion", 2)
                    print(Fore.GREEN + "Quest complete! Reward: 20 gold, 25 XP, and 2 Potions.")
                else:
                    amount = self.player.inventory.items.get("Herb", 0)
                    print(f"You have {amount}/2 Herbs. Find more and return.")
            else:
                print("Thank you for bringing those Herbs.")

        elif npc.name == "Merchant":
            print("Type shop to buy supplies.")

        elif npc.name == "Scout":
            print("Remember: you can use Potions during your adventure.")

        self.player.quest_data = self.quests.to_dict()

    def open_shop(self):
        if self.player.map_name != "castle":
            print("The Merchant is in the castle.")
            return
        merchant = next(npc for npc in NPCS if npc.name == "Merchant")
        distance = abs(merchant.x - self.player.x) + abs(merchant.y - self.player.y)
        if distance > 1:
            print("Move next to the Merchant before opening the shop.")
            return
        visit_shop(self.player)

    def start_boss_battle(self):
        if self.player.game_won:
            return
        print(Fore.RED + Style.BRIGHT + "\nThe Crystal Guardian awakens!")
        if battle(self.player, Boss()):
            self.quests.main_stage = 4
            self.player.game_won = True
            self.player.quest_data = self.quests.to_dict()

    def save(self):
        self.player.quest_data = self.quests.to_dict()
        save_player(self.player.username, self.player.to_dict())
        print(Fore.GREEN + "Game saved.")

    def show_help(self):
        print("""
MOVEMENT
  w = up, a = left, s = down, d = right

COMMANDS
  talk      Talk to a nearby character
  shop      Buy items when standing near the Merchant
  inventory View your items
  use       Use a Potion or Herb to restore HP
  stats     View your character's level, HP, XP, skills, and location
  quest     View main quest and side quest progress
  save      Save your progress
  quit      Save and leave the game

QUEST
  Speak to the Elder in the forest.
  Defeat 3 monsters and return to the Elder.
  Travel through the now-open portal to the castle.
  Defeat the Crystal Guardian in the boss chamber.
""")
