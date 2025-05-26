import random
from gui.models.Bestiary import Bestiary
from gui.service.db_service import DatabaseService

class BestiaryService:
    """Service pour gérer le bestiaire et le combat."""
    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_monsters(self, player_id):
        """
        Récupère tous les monstres du bestiaire.
        """
        query = "SELECT ID, BeastName, LifePoints FROM Bestiary"
        if not self.db_service.execute_query(query):
            return []
        rows = self.db_service.fetch_all() or []
        return [Bestiary(id=r[0], name=r[1], lifePoints=r[2]) for r in rows]

    def fight_monster(self, player_id, monster_id):
        """
        Gère un combat contre un monstre :
          1) +XP
          2) Tirage d'un seul drop (or OU objet)
          3) Application du drop au Player (wallet OU inventaire)
          4) Commit + retour du résumé
        """
        if player_id is None or monster_id is None:
            raise ValueError("player_id and monster_id must not be None")

        # 1) XP
        self.db_service.execute_query(
            "SELECT LifePoints FROM Bestiary WHERE ID = %s", (monster_id,)
        )
        xp_gain = (self.db_service.fetch_one() or (0,))[0]
        self.db_service.execute_query(
            "UPDATE Player SET ExperiencePoints = ExperiencePoints + %s WHERE ID = %s",
            (xp_gain, player_id)
        )

        # 2) Gold avant combat
        self.db_service.execute_query(
            "SELECT WalletCredits FROM Player WHERE ID = %s", (player_id,)
        )
        gold_before = (self.db_service.fetch_one() or (0,))[0]

        # 3) Récupération des drops
        self.db_service.execute_query(
            "SELECT ObjectName, DropRate, Quantity FROM Rewards WHERE MonsterID = %s",
            (monster_id,)
        )
        drop_rows = self.db_service.fetch_all() or []

        # 4) Choix pondéré d'un seul drop
        gold_gained = 0
        items_gained = []
        total_rate = sum(rate for _, rate, _ in drop_rows)
        if total_rate > 0:
            r = random.random() * total_rate
            cum = 0
            for name, rate, qty in drop_rows:
                cum += rate
                if r <= cum:
                    obj_name, obj_qty = name, qty
                    if obj_name.lower() == 'gold':
                        gold_gained = obj_qty
                    else:
                        try:
                            self.db_service.execute_query(
                                "INSERT IGNORE INTO Inventory (PlayerID, ObjectName) VALUES (%s, %s)",
                                (player_id, obj_name)
                            )
                            self.db_service.commit()
                            items_gained.append((obj_name, 1))
                        except Exception:
                            pass
                    break

        # 5) Mise à jour du gold si besoin
        if gold_gained:
            self.db_service.execute_query(
                "UPDATE Player SET WalletCredits = WalletCredits + %s WHERE ID = %s",
                (gold_gained, player_id)
            )

        # 6) Commit
        self.db_service.commit()

        # 7) Relecture des stats finales
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
