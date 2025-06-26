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
                # Prevent invalid moves from base unless dice = 1 or 6
                if self.current_pos < 0 and config.DICE_FINAL_VALUE not in (1, 6):
                    print(f"❌ Invalid move: {self.pawn_id} is in base and dice is {config.DICE_FINAL_VALUE} and current turn is {config.CURRENT_PLAYER}")
                    

                    return
                
                print(f"Starting move for {self.pawn_id}")
                self.move_to(config.DICE_FINAL_VALUE)
                self.timer.start(100)
            else:
                print(f"❌ Not your turn — pawn {self.pawn_id} is inactive.")
        else:
            print("❌ Dice not rolled, already moved, or pawn is moving.")

    def move_to(self, steps):
        print(f"move_to called with steps={steps}")
        
        # Pawn in base, valid dice → move out to starting point
        if self.current_pos < 0:
            if config.DICE_FINAL_VALUE in (1, 6):
                if config.CURRENT_PLAYER == "blue":
                    self.target_pos = 0
                elif config.CURRENT_PLAYER == "green":
                    self.target_pos = 26
                else:
                    print("⚠️ Unsupported player color!")
                    return
                print(f"🎯 Moving from base to starting position: {self.target_pos}")
                return

        # Pawn already on board, calculate normal movement
        sorted_positions = sorted([k for k in self.coords if k >= 0])

        if self.current_pos not in sorted_positions:
            print(f"⚠️ current_pos {self.current_pos} not in coords keys")
            return
        
        current_index = sorted_positions.index(self.current_pos)
        target_index = current_index + steps

        if(config.CURRENT_PLAYER == 'green'):

            target_index = target_index % config.MAX_POSITIONS



        else:
            if target_index >= len(sorted_positions):
                target_index = len(sorted_positions) - 1  # cap at end
        
        self.target_pos = sorted_positions[target_index]
        print(f"🎯 Target set from {self.current_pos} to {self.target_pos}")

    def step_move(self):
        print(f"[step_move] current_pos: {self.current_pos}, target_pos: {self.target_pos}")

        if self.current_pos < 0:
            if config.DICE_FINAL_VALUE in (1, 6):
                if config.CURRENT_PLAYER == "blue":
                    self.current_pos = 0
                elif config.CURRENT_PLAYER == "green":
                    self.current_pos = 26
                self.update_position()
            else:
                self.timer.stop()
                self.parent.move_finished()
        else:
            # Green player wraps movement
            if self.color == "green":
                if self.current_pos != self.target_pos:
                    self.current_pos = (self.current_pos + 1) % config.MAX_POSITIONS
                    self.update_position()
                if self.current_pos == self.target_pos:
                    self.timer.stop()
                    self.parent.move_finished()

            # Blue player — no wrap logic
            elif self.color == "blue":
                if self.current_pos < self.target_pos:
                    self.current_pos += 1
                    self.update_position()
                if self.current_pos == self.target_pos:
                    self.timer.stop()
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

        # Calculate size of pawn relative to board size
        scale_factor = 0.05  # 5% of board size
        target_width = int(bg_width * scale_factor)
        target_height = int(bg_height * scale_factor)

        # Load and scale pawn image keeping aspect ratio
        path = os.path.join(config.ASSETS_DIR, "Pawns", f"pawn_{self.color}.png")
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.button.setIcon(QIcon(scaled))
            self.button.setIconSize(scaled.size())
            self.button.resize(scaled.size())  # Button matches image size

        # Compute final button position centered on the relative coordinates
        btn_width = self.button.width()
        btn_height = self.button.height()
        x = int(label.x() + (rel_x + 0.025) * bg_width - btn_width / 2)
        y = int(label.y() + (rel_y + 0.025) * bg_height - btn_height / 2)

        # Clamp position to window bounds
        x = max(0, min(x, self.parent.width() - btn_width))
        y = max(0, min(y, self.parent.height() - btn_height))

        self.button.move(x, y)
