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

        play_dice_sound()
        self.shuffle_count = 0
        self.button.setEnabled(False)  # Disable during roll
        self.timer.start(50)

    def shuffle(self):
        roll = random.randint(1, 6)

        if self.shuffle_count < self.max_shuffle - 1:
            config.DICE_FINAL_VALUE = roll  # Interim value
            self.set_icon(roll)
        else:
            self.final_roll = roll
            config.DICE_FINAL_VALUE = self.final_roll
            config.DICE_ROLLED = 1
            self.timer.stop()
            self.set_icon(self.final_roll)
            self.button.setEnabled(False)  # Lock dice after roll

            # ✅ Turn skipping logic
            pawn_ids = config.PLAYER_PAWNS[config.CURRENT_PLAYER]
            movable = any(self.can_pawn_move(p) for p in self.parent.pawns if p.pawn_id in pawn_ids)

            if not movable:
                print(f"🚫 {config.CURRENT_PLAYER.capitalize()} has no valid moves — skipping turn.")
                self.final_roll = None
                config.DICE_ROLLED = 0
                config.SHOULD_SWITCH_TURN = True
                config.switch_player_turn()
                self.button.setEnabled(True)  # Re-enable dice for next player
                return
            else:
                config.SHOULD_SWITCH_TURN = True
                print(f"🎯 {config.CURRENT_PLAYER}'s pawn can move. Turn will switch after pawn finishes.")

        self.shuffle_count += 1




    def can_pawn_move(self, pawn):
        if pawn.current_pos < 0:
            return self.final_roll in (1, 6)  # Can only move out of base if 1 or 6
        else:
            return True  # Already on board → always movable


    def set_icon(self, roll):
        if not roll:
            print("⚠️ Dice roll is None or 0 — skipping icon update.")
            return
        path = os.path.join(config.DICE_FOLDER, f"dice{roll}.png")
        if not os.path.exists(path):
            print(f"⚠️ Dice image not found: {path}")
        self.button.setIcon(QIcon(path))
        self.button.setIconSize(self.button.size())

    def update_position(self):
        x = (self.parent.width() - self.button.width()) // 2
        y = self.parent.height() - self.button.height() - 3
        self.button.move(x, y)