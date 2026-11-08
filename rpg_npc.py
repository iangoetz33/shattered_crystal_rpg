class NPC:
    def __init__(self, name, dialogue, map_name, x, y):
        self.name = name
        self.dialogue = dialogue
        self.map_name = map_name
        self.x = x
        self.y = y


# Five characters with their own dialogue and map locations.
NPCS = [
    NPC(
        "Elder",
        "The kingdom's crystal is gone. Defeat three monsters, then return to me.",
        "forest", 2, 1
    ),
    NPC(
        "Scout",
        "I have explored these woods. The path to the castle lies to the east.",
        "forest", 4, 4
    ),
    NPC(
        "Guard",
        "The castle needs brave fighters. Defeat two monsters and I will reward you.",
        "castle", 2, 1
    ),
    NPC(
        "Healer",
        "I need two Herbs to prepare medicine. Bring them to me for a reward.",
        "castle", 5, 3
    ),
    NPC(
        "Merchant",
        "Welcome! I sell Potions and Herbs to travelers.",
        "castle", 7, 4
    ),
]
