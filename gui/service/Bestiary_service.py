import random
from gui.models.Bestiary import Bestiary
from gui.service.db_service import DatabaseService

class BestiaryService:
    """Service for managing the bestiary."""

    def __init__(self):
        """Initialize the bestiary service."""
        self.db_service = DatabaseService()

    def get_bestiaryName(self):
        """Retrieve a bestiary entry by its ID."""
        bestiaryList = []
        query = "SELECT * FROM Bestiary"
        if not self.db_service.execute_query(query):
            return []
        
        result = self.db_service.fetch_all()
        for row in result:
            bestiaryList.append(row[1])
        return bestiaryList
    
    def get_bestiary_details(self, name):
        """Retrieve details of a specific bestiary entry by its name."""
        query = "SELECT * FROM Bestiary WHERE BeastName = %s"
        print(name)
        if not self.db_service.execute_query(query, (name,)):
            return None
        
        result = self.db_service.fetch_one()
        print(result)
        if result:
            return Bestiary(result[0], result[1], result[2], result[3], result[4], result[5])
        return None


    def reward_character_for_monster(self, character_id, monster_id):
        """
        Tue monster_id pour character_id :
         1) Récupère LifePoints (XP) et player_id lié
         2) Tire un seul objet depuis Rewards
         3) Tire de l’or depuis MonsterGold
         4) Met à jour Player (ExperiencePoints + WalletCredits)
         5) Insère l’objet en Inventory
         6) Commit et retourne {'xp','gold','items'}
        """
        db = self.db_service

        # 1) XP et player_id
        db.execute_query(
            "SELECT B.LifePoints, C.PlayerID "
            "FROM Bestiary B "
            "JOIN CharacterTable C ON C.ID = %s "
            "WHERE B.ID = %s",
            (character_id, monster_id)
        )
        row = db.fetch_one()
        if not row:
            return {'xp': 0, 'gold': 0, 'items': []}
        xp_gain, player_id = row

        # 2) Tirage objet depuis Rewards
        db.execute_query(
            "SELECT ObjectName, DropRate, Quantity FROM Rewards WHERE MonsterID = %s",
            (monster_id,)
        )
        drops = db.fetch_all() or []
        total = sum(r for _, r, _ in drops)
        pick = random.random() * total if total else 0

        items = []
        cum = 0
        for name, rate, qty in drops:
            cum += rate
            if pick <= cum and name.lower() != 'gold':
                db.execute_query(
                    """
                    INSERT INTO Inventory (PlayerID, CharacterID, ObjectName, Quantity)
                    VALUES (%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE Quantity = Quantity + %s
                    """,
                    (player_id, character_id, name, qty, qty)
                )
                items.append((name, qty))
                break

        # 3) Tirage or depuis MonsterGold
        db.execute_query(
            "SELECT GoldAmount, DropRate FROM MonsterGold WHERE MonsterID = %s",
            (monster_id,)
        )
        mg = db.fetch_one()
        gold_gain = 0
        if mg:
            gold_amount, gold_rate = mg
            if random.random() <= (gold_rate / 100.0):
                gold_gain = gold_amount

        # 4) Mise à jour du Player
        if xp_gain:
            db.execute_query(
                "UPDATE Player SET ExperiencePoints = ExperiencePoints + %s WHERE ID = %s",
                (xp_gain, player_id)
            )
        if gold_gain:
            db.execute_query(
                "UPDATE Player SET WalletCredits = WalletCredits + %s WHERE ID = %s",
                (gold_gain, player_id)
            )

        # 5) Commit et retour
        db.commit()
        return {'xp': xp_gain, 'gold': gold_gain, 'items': items}
