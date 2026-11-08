ITEMS = {
    "Potion": {"price": 10, "description": "Restores up to 35 HP."},
    "Herb": {"price": 5, "description": "Restores up to 15 HP."},
    "Crystal Shard": {"price": 0, "description": "The crystal recovered from the guardian."},
}


def healing_amount(item_name):
    healing_items = {
        "Potion": 35,
        "Herb": 15,
    }
    return healing_items.get(item_name, 0)
