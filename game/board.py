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

        self.setWindowTitle("Ludo Game")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height() - 30)
        self.label.setAlignment(Qt.AlignCenter)
        self.set_background_image()

#        self.pawn = Pawn(self, config.PAWN_COORDINATES, start_pos=-1)
        self.dice = Dice(self)
        self.pawns = []   # <-- add this line here BEFORE appending pawns
        for color, pids in config.PLAYER_PAWNS.items():
            for pid in pids:
                pawn = Pawn(self, config.PAWN_COORDINATES, pawn_id=pid, color=color)
                self.pawns.append(pawn)

    def register_pawn_click(self, pawn):
        if config.DICE_ROLLED == 1 and self.final_roll:
            pawn.move_to(self.final_roll)
            config.DICE_ROLLED = 0
            self.final_roll = None

    def move_finished(self):
        config.DICE_ROLLED = 0
        config.CURRENT_PLAYER = "green" if config.CURRENT_PLAYER == "blue" else "blue"
        print(f"Turn switched. Next player: {config.CURRENT_PLAYER}")




    def resizeEvent(self, event):
        self.set_background_image()
        self.pawn.update_position()
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


    def resizeEvent(self, event):
    # Resize background board
        self.set_background_image()

    # Resize and reposition pawn
        if hasattr(self, "pawn"):
            self.pawn.update_position()

        # Resize and reposition dice
        if hasattr(self, "dice"):
            self.dice.update_position()

        super().resizeEvent(event)




    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.print_relative_click_position(event)




    def print_relative_click_position(self, event):
        label = self.label
        bg_x = label.x()
        bg_y = label.y()
        bg_width = label.width()
        bg_height = label.height()

        click_x = event.x()
        click_y = event.y()

        # Make sure click is within the board label bounds
        if not (bg_x <= click_x <= bg_x + bg_width and bg_y <= click_y <= bg_y + bg_height):
            return  # Click outside the board

        # Calculate relative coordinates (0 to 1)
        rel_x = (click_x - bg_x) / bg_width
        rel_y = (click_y - bg_y) / bg_height

        print(f"🖱️ Clicked at (relative): x={rel_x:.3f}, y={rel_y:.3f}")
