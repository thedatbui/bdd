import random
from gui.service.inventory_service import InventoryService
from gui.models.Bestiary import Bestiary
from gui.service.db_service import DatabaseService

class BestiaryService:
    # … __init__ idem …

    def fight_monster(self, player_id, monster_id):
        if player_id is None or monster_id is None:
            raise ValueError("player_id and monster_id must not be None")

        # 1) XP gain
        self.db_service.execute_query(
            "SELECT LifePoints FROM Bestiary WHERE ID = %s", (monster_id,)
        )
        xp_gain = (self.db_service.fetch_one() or (0,))[0]
        self.db_service.execute_query(
            "UPDATE Player SET ExperiencePoints = ExperiencePoints + %s WHERE ID = %s",
            (xp_gain, player_id)
        )

        # 2) Gold avant
        self.db_service.execute_query(
            "SELECT WalletCredits FROM Player WHERE ID = %s", (player_id,)
        )
        gold_before = (self.db_service.fetch_one() or (0,))[0]

        # 3) Récupère la table de drops
        self.db_service.execute_query(
            "SELECT ObjectName, DropRate, Quantity FROM Rewards WHERE MonsterID = %s",
            (monster_id,)
        )
        drop_rows = self.db_service.fetch_all() or []

        # 4) Filtre les drops réussis
        successful_drops = []
        for obj_name, drop_rate, qty in drop_rows:
            if random.random() * 100 <= drop_rate:
                successful_drops.append((obj_name, qty))

        gold_gained = 0
        items_gained = []

        # 5) Si au moins un drop est sorti, on en choisit un
        if successful_drops:
            obj_name, qty = random.choice(successful_drops)
            if obj_name.lower() == 'gold':
                gold_gained = qty
            else:
                # ajoute qty exemplaires
                for _ in range(qty):
                    if self.inventory_service.can_add_item(player_id):
                        self.inventory_service.add_item(player_id, obj_name)
                        items_gained.append((obj_name, 1))

        # 6) Mise à jour du gold
        if gold_gained:
            self.db_service.execute_query(
                "UPDATE Player SET WalletCredits = WalletCredits + %s WHERE ID = %s",
                (gold_gained, player_id)
            )

        # 7) Commit
        self.db_service.commit()

        # 8) Relecture des stats
        self.db_service.execute_query(
            "SELECT WalletCredits, ExperiencePoints, PlayerLevel FROM Player WHERE ID = %s",
            (player_id,)
        )
        gold_after, xp_after, level_after = self.db_service.fetch_one() or (gold_before, None, None)

        return {
            'xp': xp_gain,
            'gold': gold_gained,
            'items': items_gained,
            'newLevel': level_after
        }
