from colorama import Fore


class QuestManager:
    def __init__(self):
        # Main quest stages: 0 not started, 1 defeat monsters,
        # 2 return to Elder, 3 defeat boss, 4 completed.
        self.main_stage = 0
        self.monsters_defeated = 0
        self.side_quests = {
            "monster_hunt": {
                "accepted": False, "progress": 0,
                "complete": False, "rewarded": False
            },
            "herb_search": {
                "accepted": False, "complete": False, "rewarded": False
            },
        }

    def accept_side_quest(self, quest_name):
        self.side_quests[quest_name]["accepted"] = True

    def record_monster_defeat(self):
        if self.main_stage == 1:
            self.monsters_defeated += 1
            print(f"Main quest progress: {self.monsters_defeated}/3 monsters.")
            if self.monsters_defeated >= 3:
                self.main_stage = 2
                print(Fore.GREEN + "Quest step complete. Return to the Elder.")

        hunt = self.side_quests["monster_hunt"]
        if hunt["accepted"] and not hunt["complete"]:
            hunt["progress"] += 1
            if hunt["progress"] >= 2:
                hunt["complete"] = True
                print(Fore.GREEN + "Monster Hunt complete. Return to the Guard.")

    def to_dict(self):
        return {
            "main_stage": self.main_stage,
            "monsters_defeated": self.monsters_defeated,
            "side_quests": self.side_quests,
        }

    @classmethod
    def from_dict(cls, data):
        quests = cls()
        quests.main_stage = data.get("main_stage", 0)
        quests.monsters_defeated = data.get("monsters_defeated", 0)
        quests.side_quests.update(data.get("side_quests", {}))
        return quests

    def show(self):
        print(Fore.CYAN + "\nQUEST LOG")

        main_steps = {
            0: "Find and speak to the Elder in the forest.",
            1: f"Defeat 3 monsters ({self.monsters_defeated}/3).",
            2: "Return to the Elder in the forest.",
            3: "Travel to the castle and defeat the Crystal Guardian.",
            4: "Completed! The kingdom is safe.",
        }
        print("Main quest:", main_steps[self.main_stage])

        hunt = self.side_quests["monster_hunt"]
        if hunt["accepted"]:
            print(f"Side quest - Monster Hunt: {hunt['progress']}/2 monsters.")
            if hunt["complete"]:
                print("  Reward:", "claimed" if hunt["rewarded"] else "ready to claim")

        herbs = self.side_quests["herb_search"]
        if herbs["accepted"]:
            print("Side quest - Herb Search: bring 2 Herbs to the Healer.")
            if herbs["complete"]:
                print("  Reward: claimed")
