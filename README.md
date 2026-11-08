# The Shattered Crystal - Terminal RPG

## Install

Open Terminal in this folder and run:

```bash
python3 -m pip install -r requirements.txt
```

## Start the game

```bash
python3 rpg_main.py
```

Use a real terminal window. This version uses typed commands so it is simple to run and understand.

## Controls

- `w`, `a`, `s`, `d`: move
- `talk`: speak to a nearby NPC
- `shop`: open the shop when next to the Merchant
- `inventory`: view items
- `use`: use a Potion or Herb
- `stats`: view character information
- `quest`: view quest progress
- `save`: save
- `help`: show instructions
- `quit`: save and exit

In battle, enter `attack`, `skill`, or `run`.

## Main quest

1. Find the Elder in the forest and speak to them.
2. Defeat three monsters.
3. Return to the Elder to open the castle portal.
4. Travel to the castle and reach the boss room.
5. Defeat the Crystal Guardian to win.

## Side quests

- Monster Hunt: speak to the Guard and defeat two monsters. Return to the Guard for 25 gold, 20 XP, and a Potion.
- Herb Search: speak to the Healer and bring two Herbs. The reward is 20 gold, 25 XP, and two Potions.

## Project files

- `rpg_main.py` - starts the program
- `rpg_game.py` - main game loop and game events
- `rpg_player.py` - player stats, level progression, and save data
- `rpg_monster.py` - monster types and Monster inheritance
- `rpg_skill.py` - skills and Skill inheritance
- `rpg_combat.py` - battle system
- `rpg_map.py` - map layouts, drawing, and movement checks
- `rpg_item.py` - item details and healing values
- `rpg_inventory.py` - inventory and using items
- `rpg_quest.py` - main and side quest progress
- `rpg_npc.py` - NPCs and dialogue
- `rpg_shop.py` - buying items
- `rpg_database.py` - TinyDB account and save storage
- `rpg_auth.py` - registration and login
- `requirements.txt` - packages needed to run the game

## Save data

TinyDB creates `rpg_save.json` after the first account is registered. It stores account information and game progress. Progress includes level, XP, gold, HP, inventory, skills, cooldowns, current map and position, quest progress, and opened chests.

Keep `rpg_save.json` in the same folder as the Python files. It is created when you play; it is not one of the files you need to create yourself.
