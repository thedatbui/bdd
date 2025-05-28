from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from gui.components.labels import *
from gui.components.butttons import *
from gui.utils import *
from gui.service.Bestiary_service import BestiaryService
from gui.service.character_service import CharacterService

class BestiaryScreen:
    """Screen for displaying the bestiary."""

    def __init__(self, main_window, scene_manager):
        """
        Initialize the bestiary screen.

        Args:
            main_window: The application's main window
            scene_manager: The scene manager for switching screens
        """
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.main_layout = main_window.mainLayout
        self.bestiary_service = BestiaryService()
        self.character_service = CharacterService()
        
    def setupBestiaryMenu(self):
        """Initialize the user interface."""
        clear_screen(self.main_layout)
        self.currentUser = self.main_window.current_user
        self.character = self.currentUser.getCharacterSelected()
        self.characterId = self.character.getAttribute("Id")
        self.questSelected = self.character_service.get_selected_quest(self.characterId) 
        self.beast = None
        self.count = 0
        self.beastKilled = 0
        if self.questSelected:
            self.beast = self.character_service.get_beast_to_kill(self.characterId, self.questSelected)
            self.count = self.character_service.get_count(self.questSelected)
            self.beastKilled = self.character_service.get_beast_killed(self.characterId, self.questSelected)

        self.label = create_title_label(f"Bestiary")
        self.main_layout.addWidget(self.label)

        self.keysLayout = add_horizontal_labels(self.main_layout, "Quest: ", "Beast: ")
        self.questLabel = self.keysLayout[0]
        self.questLabel.setText(f"Quest: {self.questSelected if self.questSelected else 'None'}")
        self.beastLabel = self.keysLayout[1]
        self.beastLabel.setText(f"Beast: {self.beast if self.beast else 'None'}")
        
        self.countLayout = add_horizontal_labels(self.main_layout, "Count Objective: ", "Beast Killed: ")
        self.countLabel = self.countLayout[0]
        self.countLabel.setText(f"Count Objective: {self.count}")
        self.beastKilledLabel = self.countLayout[1]
        self.beastKilledLabel.setText(f"Beast Killed: {self.beastKilled}")

        self.bestiaryListLayout = QHBoxLayout()
        self.bestiaryList = QtWidgets.QListWidget()
        self.bestiary = self.bestiary_service.get_bestiaryName()

        for bestiary in self.bestiary:
            item = QtWidgets.QListWidgetItem(bestiary)
            item.setData(Qt.UserRole, bestiary)
            if self.beast and bestiary == self.beast:
                item.setText(f"► {bestiary} ◄")  # Add arrow indicators
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                item.setForeground(QtGui.QColor("blue"))  # Change text color
            self.bestiaryList.addItem(item)
        
        self.bestiaryListLayout.addWidget(self.bestiaryList)
        self.bestiaryList.currentItemChanged.connect(self.on_itemChanged)

        self.label = create_label("Bestiary Details", 10, "blue", Qt.AlignTop | Qt.AlignLeft)
        self.bestiaryListLayout.addWidget(self.label)
        self.main_layout.addLayout(self.bestiaryListLayout)

        self.buttonList = add_horizontal_buttons(self.main_layout, (200, 50), "Back", "Kill")
        back_button = self.buttonList[0]
        back_button.clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))
        self.kill_button = self.buttonList[1]
        self.kill_button.setEnabled(False)
        self.kill_button.setStyleSheet("background-color: lightgray;")
        self.kill_button.clicked.connect(self.kill_monster)

    def on_itemChanged(self, current, previous):
        """Handle changes in the selected bestiary item."""
        if current:
            if self.questSelected is not None and self.beast is not None:
                self.kill_button.setEnabled(True)
                self.kill_button.setStyleSheet("background-color: lightblue;")
                
            bestiary_name = current.data(Qt.UserRole)
            bestiary = self.bestiary_service.get_bestiary_details(bestiary_name)
            details = f"Name: {bestiary.getName()}\n" \
                        f"Attributes: {bestiary.getAttributes()}\n" \
                        f"Attack: {bestiary.getAttack()}\n" \
                        f"Defense: {bestiary.getDefense()}\n" \
                        f"Life Points: {bestiary.getLifePoints()}"
            self.label.setText(details)
    

    def kill_monster(self):
        """Handle the action of killing a monster."""
        # 1) Récupérer le nom de la bête sélectionnée
        beast_name = self.bestiaryList.currentItem().data(Qt.UserRole)
        if beast_name != self.beast:
            QMessageBox.warning(self.main_window, "Erreur", "Sélectionnez la bonne bête.")
            return

        # 2) Lookup de monster_id
        self.bestiary_service.db_service.execute_query(
            "SELECT ID FROM Bestiary WHERE BeastName = %s",
            (beast_name,)
        )
        monster_id_row = self.bestiary_service.db_service.fetch_one()
        if not monster_id_row:
            QMessageBox.critical(self.main_window, "Erreur", "Monstre introuvable en base.")
            return
        monster_id = monster_id_row[0]

        # 3) Appel de la méthode de récompense (XP + loot)
        result = self.bestiary_service.reward_character_for_monster(
            self.characterId,
            monster_id
        )

        # 4) Affichage du résumé
        msg_lines = [
            f"You defeated « {beast_name} »!",
            f"XP gained: {result['xp']}"
        ]
        if result['gold']:
            msg_lines.append(f"Gold gained: {result['gold']}")
        for name, qty in result['items']:
            msg_lines.append(f"{qty}× {name}")

        # Ajouter les informations de niveau si un level up a eu lieu
        if result['level_up']:
            level_up = result['level_up']
            msg_lines.extend([
                "",
                f"Level Up! {level_up['old_level']} → {level_up['new_level']}",
                f"New inventory slots: {10 + (2 * (level_up['new_level'] - 1))}",
                f"XP for next level: {level_up['next_level_xp']}"
            ])
            # Mettre à jour le niveau dans l'objet Player
            self.currentUser.setLevel(level_up['new_level'])
            self.currentUser.setInventorySlot(10 + (2 * (level_up['new_level'] - 1)))

        QMessageBox.information(
            self.main_window,
            "Combat Rewards",
            "\n".join(msg_lines)
        )

        # 5) Rafraîchir le label d'or (s'il existe)
        if hasattr(self, 'goldLabel'):
            new_gold = self.character_service.get_wallet_for_character(self.characterId)
            self.goldLabel.setText(f"Gold: {new_gold}")

        # 6) Mise à jour de la progression de quête
        if self.beastKilled < self.count:
            self.character_service.update_beast_killed(
                self.characterId,
                self.questSelected,
                self.beastKilled + 1
            )
            self.beastKilled += 1
            self.beastKilledLabel.setText(f"Beast Killed: {self.beastKilled}")

            if self.beastKilled == self.count:
                QMessageBox.information(self.main_window, "Quête terminée",
                                        "Félicitations !")
                self.character_service.remove_quest(self.characterId, self.questSelected)
                self.character_service.select_next_quest(self.characterId)
                self.setupBestiaryMenu()

