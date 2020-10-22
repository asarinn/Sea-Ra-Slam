import json

# Third party imports
from PyQt5.QtWidgets import (QMainWindow)

# Local imports
from main_window_init import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Basic pyqt init for gui window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.configuration = json.load(open("configuration.json", "r"))

        # Class variables to hold state of check boxes
        self.two_handed_enabled = True
        self.inspire_courage_enabled = False
        self.haste_enabled = False
        self.raging_enabled = False
        self.power_attack_enabled = False
        self.enlarged_enabled = False
        self.surprise_accuracy_enabled = False
        self.powerful_blow_enabled = False
        self.flanking_enabled = False
        self.deadly_juggernaut_enabled = False

        # Connections to toggle state on check box click
        self.ui.two_handed_check_box.clicked.connect(self.two_handed_toggled)
        self.ui.inspire_courage_check_box.clicked.connect(self.inspire_courage_toggled)
        self.ui.haste_check_box.clicked.connect(self.haste_toggled)
        self.ui.raging_check_box.clicked.connect(self.raging_toggled)
        self.ui.power_attack_check_box.clicked.connect(self.power_attack_toggled)
        self.ui.enlarged_check_box.clicked.connect(self.enlarged_toggled)
        self.ui.surprise_accuracy_check_box.clicked.connect(self.surprise_accuracy_toggled)
        self.ui.powerful_blow_check_box.clicked.connect(self.powerful_blow_toggled)
        self.ui.flanking_bonus_check_box.clicked.connect(self.flanking_toggled)
        self.ui.deadly_juggernaut_check_box.clicked.connect(self.deadly_juggernaut_toggled)

        # Auto update when spin box toggled
        self.ui.kills_spin_box.valueChanged.connect(self.update_output)
        self.ui.num_hits_spin_box.valueChanged.connect(self.update_output)

        # Initialize output with initial settings
        self.update_output()

    def two_handed_toggled(self, state):
        self.two_handed_enabled = state
        self.update_output()

    def inspire_courage_toggled(self, state):
        self.inspire_courage_enabled = state
        self.update_output()

    def haste_toggled(self, state):
        self.haste_enabled = state
        self.update_output()

    def raging_toggled(self, state):
        self.raging_enabled = state
        self.update_output()

    def power_attack_toggled(self, state):
        self.power_attack_enabled = state
        self.update_output()

    def enlarged_toggled(self, state):
        self.enlarged_enabled = state
        self.update_output()

    def surprise_accuracy_toggled(self, state):
        self.surprise_accuracy_enabled = state
        self.update_output()

    def powerful_blow_toggled(self, state):
        self.powerful_blow_enabled = state
        self.update_output()

    def flanking_toggled(self, state):
        self.flanking_enabled = state
        self.update_output()

    def deadly_juggernaut_toggled(self, state):
        self.deadly_juggernaut_enabled = state
        self.update_output()

    def update_output(self):
        # Calculate strength bonus
        strength = self.configuration['STR']
        if self.raging_enabled:
            strength += self.configuration['RAGE_STR_BONUS']
        if self.enlarged_enabled:
            strength += self.configuration['ENLARGE_STR_BONUS']
        effective_strength_bonus = int((strength - 10) / 2)

        # Calculate number of attacks
        num_attacks = 1 + int((self.configuration['BAB'] - 1) / 5)

        # Calculate atack bonus
        attack_bonus = self.calculate_attack_bonus(effective_strength_bonus)

        attack_text = f' Attack Bonus: +{attack_bonus}'
        if self.haste_enabled:
            attack_text = attack_text + f'/{attack_bonus}'
        for i in range(num_attacks - 1):
            attack_text = attack_text + f'/{attack_bonus - (5 * (i + 1))}'
        self.ui.attack_bonus_label.setText(attack_text)

        # Set new spin box max
        spin_max = num_attacks
        if self.haste_enabled:
            spin_max += 1
        self.ui.num_hits_spin_box.setMaximum(spin_max)

        # Get num hits
        num_hits = int(self.ui.num_hits_spin_box.value())

        # Calculate damage
        die, damage = self.calculate_damage(effective_strength_bonus)
        damage *= num_hits
        self.ui.damage_label.setText(f'Damage: {num_hits * die[0]}d{die[1]} + {damage}')

        crit_mod = self.configuration["WEAPON_CRITICAL_MOD"]
        self.ui.crit_damage_label.setText(
            f'Critical Damage: {num_hits * crit_mod * die[0]}d{die[1]} + {crit_mod * damage}')

    def calculate_attack_bonus(self, effective_strength_bonus):
        attack_bonus = self.configuration['BAB'] + self.configuration['WEAPON_BONUS'] + effective_strength_bonus

        if self.inspire_courage_enabled:
            attack_bonus += self.configuration['INSPIRE']

        if self.haste_enabled:
            attack_bonus += self.configuration['HASTE']

        if self.power_attack_enabled:
            attack_bonus += self.configuration['POWER_ATTACK_ATTACK']

        if self.enlarged_enabled:
            attack_bonus += self.configuration['ENLARGE']

        if self.surprise_accuracy_enabled:
            attack_bonus += self.configuration['SURPRISE_ACCURACY']

        if self.flanking_enabled:
            attack_bonus += self.configuration['FLANKING']

        if self.deadly_juggernaut_enabled:
            attack_bonus += self.ui.kills_spin_box.value()

        return attack_bonus

    def calculate_damage(self, effective_strength_bonus):
        damage = self.configuration['WEAPON_BONUS']

        strength_damage = effective_strength_bonus
        if self.two_handed_enabled:
            strength_damage = int(strength_damage * self.configuration['TWO_HANDED_MULTI'])
        damage += strength_damage

        if self.powerful_blow_enabled:
            damage += self.configuration['POWERFUL_BLOW']

        power_attack_damage = 6
        if self.two_handed_enabled:
            power_attack_damage = int(power_attack_damage * self.configuration['TWO_HANDED_MULTI'])
        if self.power_attack_enabled:
            damage += power_attack_damage

        if self.inspire_courage_enabled:
            damage += self.configuration['INSPIRE']

        if self.deadly_juggernaut_enabled:
            damage += self.ui.kills_spin_box.value()

        if self.enlarged_enabled:
            die = self.configuration['ENLARGE_DAMAGE_DIE']
        else:
            die = self.configuration['DAMAGE_DIE']

        return die, damage
