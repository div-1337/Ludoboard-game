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

        config.DICE_ROLLED = 0
        config.DICE_FINAL_VALUE = None  # Start unset

    def on_click(self):
        if self.timer.isActive():
            return  # prevent double click during animation
        play_dice_sound()
        self.shuffle_count = 0
        config.DICE_FINAL_VALUE = None  # Clear previous value
        config.DICE_ROLLED = 0
        self.timer.start(50)

    def shuffle(self):
        roll = random.randint(1, 6)

        if self.shuffle_count < self.max_shuffle - 1:
            self.set_icon(roll)  # Show animation frame (not final value)
        else:
            self.final_roll = roll
            config.DICE_FINAL_VALUE = self.final_roll
            config.DICE_ROLLED = 1
            self.timer.stop()
            self.set_icon(self.final_roll)

            # Validate move eligibility
            if config.CURRENT_PLAYER == "blue":
                blue_positions = [p.current_pos for p in self.parent.pawns if p.pawn_id in (-1, -2, -3, -4)]
                if all(pos < 0 for pos in blue_positions) and self.final_roll not in (1, 6):
                    print("🚫 Blue has no valid moves — skipping turn.")
                    config.switch_player_turn()
                    return

            elif config.CURRENT_PLAYER == "red":
                red_positions = [p.current_pos for p in self.parent.pawns if p.pawn_id in (-5, -6, -7, -8)]
                if all(pos < 0 for pos in red_positions) and self.final_roll not in (1, 6):
                    print("🚫 Red has no valid moves — skipping turn.")
                    config.switch_player_turn()
                    return

            elif config.CURRENT_PLAYER == "green":
                green_positions = [p.current_pos for p in self.parent.pawns if p.pawn_id in (-9, -10, -11, -12)]
                if all(pos < 0 for pos in green_positions) and self.final_roll not in (1, 6):
                    print("🚫 Green has no valid moves — skipping turn.")
                    config.switch_player_turn()
                    return

            elif config.CURRENT_PLAYER == "yellow":
                yellow_positions = [p.current_pos for p in self.parent.pawns if p.pawn_id in (-13, -14, -15, -16)]
                if all(pos < 0 for pos in yellow_positions) and self.final_roll not in (1, 6):
                    print("🚫 Yellow has no valid moves — skipping turn.")
                    config.switch_player_turn()
                    return

        self.shuffle_count += 1

    def set_icon(self, roll):
        path = os.path.join(config.DICE_FOLDER, f"dice{roll}.png")
        self.button.setIcon(QIcon(path))
        self.button.setIconSize(self.button.size())

    def update_position(self):
        x = (self.parent.width() - self.button.width()) // 2
        y = self.parent.height() - self.button.height() - 3
        self.button.move(x, y)
