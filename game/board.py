from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon
import config
from game.pawn import Pawn
from game.dice import Dice
from game.sound import play_dice_sound

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pawns = []
        self.setWindowTitle("Ludo Game")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height() - 30)
        self.label.setAlignment(Qt.AlignCenter)
        self.set_background_image()

        self.dice = Dice(self)

        for color, pids in config.PLAYER_PAWNS.items():
            for pid in pids:
                pawn = Pawn(self, config.PAWN_COORDINATES, pawn_id=pid, color=color)
                self.pawns.append(pawn)

        # Register callback for turn switch highlight refresh
        config.TURN_CALLBACK = self.on_turn_switch

    def register_pawn_click(self, pawn):
        if config.DICE_ROLLED == 1 and self.final_roll:
            pawn.move_to(self.final_roll)
            config.DICE_ROLLED = 0
            self.final_roll = None

    def move_finished(self):
        config.DICE_ROLLED = 0
        config.CURRENT_PLAYER = "green" if config.CURRENT_PLAYER == "blue" else "blue"
        print(f"Turn switched. Next player: {config.CURRENT_PLAYER}")

    def is_safe_zone(self, pos):
        return pos in config.SAFE_ZONES


    def resizeEvent(self, event):
        self.set_background_image()

        for pawn in self.pawns:
            pawn.update_position()

        self.dice.update_position()

        super().resizeEvent(event)

    def set_background_image(self):
        pixmap = QPixmap(config.BOARD_IMAGE)
        if pixmap.isNull():
            print("Failed to load image")
            return

        scaled_pixmap = pixmap.scaled(self.width(), self.height() - 50, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height() - 75)


    def on_turn_switch(self):
        for pawn in self.pawns:
            pawn.update_position()

    