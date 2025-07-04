from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import config
import random
import os
from game.sound import play_dice_sound

class Dice:
    def __init__(self, parent):
        self.parent = parent
        self.button = QPushButton(parent)
        self.button.resize(75, 75)
        self.update_position()
        self.button.clicked.connect(self.on_click)
        self.timer = QTimer()
        self.timer.timeout.connect(self.shuffle)
        self.shuffle_count = 0
        self.max_shuffle = 6
        self.final_roll = None

    def on_click(self):
        if config.DICE_ROLLED == 1:
            print("⛔ Dice already rolled. Move a pawn before rolling again.")
            return

        # ✅ Reset turn switch by default. Player must re-earn it (by cut, finish, or entering from base)
        config.SHOULD_SWITCH_TURN = True

        play_dice_sound()
        self.shuffle_count = 0
        self.final_roll = None
        config.DICE_FINAL_VALUE = None
        self.button.setEnabled(False)
        self.timer.start(50)

    def shuffle(self):
        roll = random.randint(1, 6)

        if self.shuffle_count < self.max_shuffle - 1:
            config.DICE_FINAL_VALUE = roll
            self.set_icon(roll)
        else:
            self.final_roll = roll
            config.DICE_FINAL_VALUE = roll
            config.DICE_ROLLED = 1
            self.timer.stop()
            self.set_icon(roll)

            print(f"🎲 Final roll = {roll} for {config.CURRENT_PLAYER}")

            # ✅ Check if player has no valid moves
            if not self.has_valid_move():
                print(f"🚫 {config.CURRENT_PLAYER.capitalize()} has no valid moves — skipping turn.")
                config.DICE_FINAL_VALUE = None
                config.DICE_ROLLED = 0
                config.SHOULD_SWITCH_TURN = True
                config.switch_player_turn(callback=self.parent.on_turn_switch)
                self.button.setEnabled(True)

        self.shuffle_count += 1

    def has_valid_move(self):
        pawn_ids = config.PLAYER_PAWNS[config.CURRENT_PLAYER]
        for pawn in self.parent.pawns:
            if pawn.pawn_id in pawn_ids and self.can_pawn_move(pawn):
                return True
        return False

    def can_pawn_move(self, pawn):
        if config.DICE_FINAL_VALUE is None:
            return False

        if pawn.pawn_id not in config.PLAYER_PAWNS[config.CURRENT_PLAYER]:
            return False

        pos = pawn.current_pos
        dice_value = config.DICE_FINAL_VALUE

        if pos < 0:
            return dice_value in (1, 6)

        finish_paths = {
            "blue": config.BLUE_FINISH,
            "red": config.RED_FINISH,
            "green": config.GREEN_FINISH,
            "yellow": config.YELLOW_FINISH
        }
        finish_path = finish_paths[config.CURRENT_PLAYER]

        if pos in finish_path:
            idx = finish_path.index(pos)
            return idx + dice_value < len(finish_path)

        entry_index = config.ENTRY_INDEX[config.CURRENT_PLAYER]
        sorted_positions = sorted(k for k in config.PAWN_COORDINATES if k >= 0)
        if pos not in sorted_positions:
            return False

        current_index = sorted_positions.index(pos)
        target_index = current_index + dice_value

        if current_index < entry_index <= target_index:
            offset = target_index - (entry_index + 1)
            return offset < len(finish_path)

        return True

    def set_icon(self, roll):
        if not roll:
            print("⚠️ Dice roll is None or 0 — skipping icon update.")
            return
        path = os.path.join(config.DICE_FOLDER, f"dice{roll}.png")
        if not os.path.exists(path):
            print(f"⚠️ Dice image not found: {path}")
        else:
            self.button.setIcon(QIcon(path))
            self.button.setIconSize(self.button.size())

    def update_position(self):
        x = (self.parent.width() - self.button.width()) // 2
        y = self.parent.height() - self.button.height() - 3
        self.button.move(x, y)
