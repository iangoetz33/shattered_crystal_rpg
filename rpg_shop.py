from colorama import Fore
from rpg_item import ITEMS


def visit_shop(player):
    print(Fore.CYAN + "\nMERCHANT SHOP")
    print("Gold:", player.gold)
    for name, info in ITEMS.items():
        if info["price"] > 0:
            print(f"{name} - {info['price']} gold: {info['description']}")

    print("Enter an item name to buy, or type leave.")
    while True:
        choice = input("Shop > ").strip().title()

        if choice == "Leave":
            print("You leave the shop.")
            return

        if choice not in ITEMS or ITEMS[choice]["price"] <= 0:
            print("That item is not sold here.")
            continue

        price = ITEMS[choice]["price"]
        if player.gold < price:
            print("You do not have enough gold.")
        else:
            player.gold -= price
            player.inventory.add(choice)
            print(Fore.GREEN + f"You bought 1 {choice}.")
