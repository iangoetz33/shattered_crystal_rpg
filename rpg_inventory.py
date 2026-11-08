from colorama import Fore
from rpg_item import healing_amount


class Inventory:
    def __init__(self, items=None):
        self.items = items if items is not None else {}

    def add(self, item_name, amount=1):
        self.items[item_name] = self.items.get(item_name, 0) + amount

    def remove(self, item_name, amount=1):
        if self.items.get(item_name, 0) < amount:
            return False

        self.items[item_name] -= amount
        if self.items[item_name] == 0:
            del self.items[item_name]
        return True

    def to_dict(self):
        return self.items.copy()


def show_inventory(player):
    print(Fore.CYAN + "\nINVENTORY")
    if not player.inventory.items:
        print("Your inventory is empty.")
        return

    for item_name, amount in player.inventory.items.items():
        print(f"{item_name}: {amount}")


def use_item(player):
    show_inventory(player)
    item_name = input("Which item do you want to use? ").strip().title()
    healing = healing_amount(item_name)

    if healing == 0:
        print("That item cannot be used.")
        return

    if not player.inventory.remove(item_name):
        print("You do not have that item.")
        return

    restored = min(healing, player.max_hp - player.hp)
    player.hp += restored
    print(Fore.GREEN + f"You restored {restored} HP.")
