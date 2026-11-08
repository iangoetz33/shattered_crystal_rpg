from colorama import Fore
from rpg_skill import get_skill


def battle(player, monster):
    print(Fore.RED + f"\nA battle with {monster.name} begins!")

    while player.hp > 0 and monster.hp > 0:
        print(f"\nYour HP: {player.hp}/{player.max_hp}")
        print(f"{monster.name} HP: {max(0, monster.hp)}")
        print("Actions: attack | skill | run")
        action = input("Battle > ").strip().lower()

        if action == "attack":
            damage = 12 + (player.level * 2)
            monster.hp -= damage
            print(f"You attack for {damage} damage.")

        elif action == "skill":
            print("Learned skills:", ", ".join(player.skills))
            skill_name = input("Enter skill name, or type cancel: ").strip()
            if skill_name.lower() == "cancel":
                continue
            if skill_name not in player.skills:
                print("You have not learned that skill.")
                continue
            if player.cooldowns.get(skill_name, 0) > 0:
                print(f"{skill_name} has {player.cooldowns[skill_name]} turn(s) left on cooldown.")
                continue

            skill = get_skill(skill_name)
            player.cooldowns[skill_name] = skill.use(player, monster)

        elif action == "run":
            if monster.name == "Crystal Guardian":
                print("You cannot run away from the Final Boss.")
                continue
            print("You escaped from the battle.")
            return False

        else:
            print("Please enter attack, skill, or run.")
            continue

        if monster.hp <= 0:
            break

        damage = monster.attack()
        player.hp -= damage
        print(Fore.RED + f"The {monster.name} attacks you for {damage} damage.")

        # Cooldowns decrease after each completed player turn.
        for name in player.cooldowns:
            if player.cooldowns[name] > 0:
                player.cooldowns[name] -= 1

    if player.hp <= 0:
        return False

    print(Fore.GREEN + f"\nYou defeated {monster.name}!")
    player.gold += monster.gold
    player.gain_xp(monster.xp)
    if monster.drop:
        player.inventory.add(monster.drop)
        print(f"It dropped: {monster.drop}")
    return True
