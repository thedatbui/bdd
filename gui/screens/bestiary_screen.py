import random
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QPushButton
from gui.utils import clear_screen, setupLabel, setupButtons, getCurrentUser
from gui.service.bestiary_service import BestiaryService

class BestiaryScreen:
    """Affiche le bestiaire et gère le combat contre un monstre."""
    def __init__(self, main_window, scene_manager):
        self.main_window = main_window
        self.scene_manager = scene_manager
        self.layout = main_window.mainLayout
        self.bestiary_service = BestiaryService()

    def setupBestiaryMenu(self):
        clear_screen(self.layout)
        setupLabel(self.layout, "-- Bestiaire --")

        user = self.main_window.current_user
        character = user.getCharacterSelected()
        if character is None :
            print(character)
            QMessageBox.warning(
                self.main_window,
                "Erreur",
                "Vous devez d’abord sélectionner un personnage."
            )
            # retour automatique au menu principal
            self.scene_manager.switch_to_menu("Main Menu")
            return

        # Chargement des monstres
        monsters = self.bestiary_service.get_all_monsters(user.getId())
        if not monsters:
            QMessageBox.warning(
                self.main_window,
                "Erreur",
                "Aucun monstre en base !"
            )
            return

        self.list_widget = QListWidget()
        for m in monsters:
            self.list_widget.addItem(f"{m.id} – {m.name} (PV: {m.lifePoints})")
        self.layout.addWidget(self.list_widget)

        # Boutons de combat
        select_btn, random_btn, back_btn = setupButtons(
            self.layout, (200, 50),
            "Combattre sélectionné", "Combattre aléatoire", "Retour au menu"
        )
        select_btn.clicked.connect(self.fight_selected_monster)
        random_btn.clicked.connect(self.fight_random_monster)
        back_btn.clicked.connect(lambda: self.scene_manager.switch_to_menu("Main Menu"))

    def fight_selected_monster(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            QMessageBox.warning(self.main_window, "Erreur", "Veuillez sélectionner un monstre.")
            return
        self._fight(idx)

    def fight_random_monster(self):
        user=self.main_window.current_user
        monsters = self.bestiary_service.get_all_monsters(user.getId()) if user else []
        if not monsters:
            QMessageBox.warning(self.main_window, "Erreur", "Aucun monstre en base !")
            return
        rand_idx = random.randrange(len(monsters))
        self._fight(rand_idx)

    def _fight(self, monster_index: int):
        user=self.main_window.current_user   
        if not user:
            QMessageBox.warning(self.main_window, "Erreur", "Problème : aucun utilisateur connecté.")
            self.scene_manager.switch_to_menu("Main Menu")
            return

        # On recharge la liste pour être sûr de l'ordre
        monsters = self.bestiary_service.get_all_monsters(user.getId())
        monster = monsters[monster_index]

        # Combat via le service (utilisateur)
        result = self.bestiary_service.fight_monster(user.getId(), monster.id)

        # Affichage du récapitulatif
        msg = (
            f"Vous avez vaincu « {monster.name} » !\n"
            f"+{result['xp']} XP (niveau {result['newLevel']})\n"
            f"+{result['gold']} or\n"
        )
        if result['items']:
            items_str = ', '.join(f"{name} x{qty}" for name, qty in result['items'])
            msg += f"Objets: {items_str}"
        QMessageBox.information(self.main_window, "Combat terminé", msg)
