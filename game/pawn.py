from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt
import config
import os
import traceback

class Pawn:

    def __init__(self, parent, coords, pawn_id, color):
        self.pawn_id = pawn_id
        self.color = color
        self.parent = parent
        self.steps = coords
        self.coords = coords
        self.current_pos = pawn_id
        self.target_pos = pawn_id

        self.moving = False  # Flag to track if pawn is currently moving

        self.button = QPushButton(parent)
        self.button.setFlat(True)
        self.button.setStyleSheet("background-color: rgba(0,0,0,0); border: none;")
        self.button.resize(50, 50)
        self.load_image()

        self.timer = QTimer(self.parent)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.step_move)

        self.button.clicked.connect(self.on_click)

        self.update_position()

    def on_click(self):
        print(f"on_click called for pawn {self.pawn_id} with dice value {config.DICE_FINAL_VALUE}")
        if config.DICE_ROLLED == 1 and not self.timer.isActive():
            allowed_ids = config.PLAYER_PAWNS[config.CURRENT_PLAYER]
            if self.pawn_id in allowed_ids:
                print(f"Starting move for {self.pawn_id}")
                self.move_to(config.DICE_FINAL_VALUE)
                self.timer.start(100)
                # Do NOT reset DICE_ROLLED or switch player here, wait until move fully finishes
            else:
                print(f"❌ Not your turn — pawn {self.pawn_id} is inactive.")
        else:
            print("❌ Dice not rolled, already moved, or pawn is moving.")

    def move_to(self, steps):
        print(f"move_to called with steps={steps}")

        # Get all valid positions sorted
        sorted_positions = sorted(self.coords.keys())
        
        if self.current_pos not in sorted_positions:
            print(f"⚠️ current_pos {self.current_pos} not in coords keys")
            return
        
        current_index = sorted_positions.index(self.current_pos)
        target_index = current_index + steps

        if target_index >= len(sorted_positions):
            target_index = len(sorted_positions) - 1  # cap at end
        
        self.target_pos = sorted_positions[target_index]

        print(f"Target set from {self.current_pos} to {self.target_pos}")


    def step_move(self):
        if self.current_pos < self.target_pos:
            self.current_pos += 1
            self.update_position()
        else:
            self.timer.stop()
            # Notify game that move ended, so dice state resets and turn switches
            self.parent.move_finished()



    def load_image(self):
        path = os.path.join(config.ASSETS_DIR, "Pawns", f"pawn_{self.color}.png")
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.button.setIcon(QIcon(pixmap))
            self.button.setIconSize(self.button.size())

    def update_position(self):
        label = self.parent.label
        bg_width = label.width()
        bg_height = label.height()

        if self.current_pos not in self.coords:
            print(f"⚠️ Invalid position: {self.current_pos}")
            return

        rel_x, rel_y = self.coords[self.current_pos]

        scale_factor = 0.05
        pawn_width = int(bg_width * scale_factor)
        pawn_height = int(bg_height * scale_factor)
        self.button.resize(pawn_width, pawn_height)

        x = int(label.x() + rel_x * bg_width)
        y = int(label.y() + rel_y * bg_height)
        self.button.move(x, y)

        path = os.path.join(config.ASSETS_DIR, "Pawns", f"pawn_{self.color}.png")
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(pawn_width, pawn_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.button.setIcon(QIcon(scaled))
            self.button.setIconSize(self.button.size())
