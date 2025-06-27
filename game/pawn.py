from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt
import config
import os

class Pawn:
    def __init__(self, parent, coords, pawn_id, color):
        self.pawn_id = pawn_id
        self.color = color
        self.parent = parent
        self.steps = coords
        self.coords = coords
        self.current_pos = pawn_id
        self.target_pos = pawn_id

        self.button = QPushButton(parent)
        self.button.setFlat(True)
        self.button.setStyleSheet("background-color: rgba(0,0,0,0); border: none;")
        self.button.resize(50, 50)
        self.load_image()

        self.timer = QTimer(self.parent)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.step_move)

        self.button.clicked.connect(self.on_click)

        self.moving = False
        self.update_position()

    def on_click(self):
        if config.DICE_FINAL_VALUE is None:
            print("⚠️ Dice has not been rolled yet!")
            return

        print(f"on_click called for pawn {self.pawn_id} with dice value {config.DICE_FINAL_VALUE}")

        if config.DICE_ROLLED == 1 and not self.timer.isActive():
            allowed_ids = config.PLAYER_PAWNS[config.CURRENT_PLAYER]

            if self.pawn_id in allowed_ids:
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

        # 🚀 First roll-out from base
        if self.current_pos < 0 and config.DICE_FINAL_VALUE in (1, 6):
            start_positions = {
                "blue": 0, "red": 13, "green": 26, "yellow": 39
            }
            self.target_pos = start_positions.get(config.CURRENT_PLAYER)
            print(f"🎯 Moving from base to starting position: {self.target_pos}")
            self.current_pos = self.target_pos
            self.update_position()
            self.timer.stop()
            config.DICE_ROLLED = 0
            config.DICE_FINAL_VALUE = 0
            if config.SHOULD_SWITCH_TURN:
                config.SHOULD_SWITCH_TURN = False
                config.switch_player_turn()
            return

        sorted_positions = sorted(k for k in self.coords if k >= 0)
        if self.current_pos not in sorted_positions:
            print(f"⚠️ current_pos {self.current_pos} not in coords keys")
            return

        current_index = sorted_positions.index(self.current_pos)
        target_index = current_index + steps

        # 🔄 Wrap-around for GREEN, RED, YELLOW
        if config.CURRENT_PLAYER in ('green', 'red', 'yellow'):
            target_index %= len(sorted_positions)  # wrap using modulo :contentReference[oaicite:1]{index=1}
            self.target_pos = sorted_positions[target_index]
        else:
            # 🔹 BLUE: cap at end (until we implement its safe path beyond 50)
            if target_index >= len(sorted_positions):
                target_index = len(sorted_positions) - 1
            self.target_pos = sorted_positions[target_index]

        print(f"🎯 Target set from {self.current_pos} to {self.target_pos}")


    def step_move(self):
        print(f"[step_move] current_pos: {self.current_pos}, target_pos: {self.target_pos}")

        if self.current_pos < 0:
            self.timer.stop()
            return

        if self.color in ["red", "green", "yellow"]:
            if self.current_pos != self.target_pos:
                self.current_pos = (self.current_pos + 1) % config.MAX_POSITIONS
                self.update_position()
            if self.current_pos == self.target_pos:
                self.timer.stop()
                config.DICE_ROLLED = 0
                config.DICE_FINAL_VALUE = 0
                if config.SHOULD_SWITCH_TURN:
                    config.SHOULD_SWITCH_TURN = False
                    print(f"🧠 Requesting turn switch from pawn {self.pawn_id} of color {self.color}")
                    config.switch_player_turn()
                self.check_collision()
                self.parent.dice.button.setEnabled(True)  # Re-enable dice
                    
        else:
            if self.current_pos < self.target_pos:
                self.current_pos += 1
                self.update_position()
            if self.current_pos == self.target_pos:
                self.timer.stop()
                config.DICE_ROLLED = 0
                config.DICE_FINAL_VALUE = 0
                if config.SHOULD_SWITCH_TURN:
                    config.SHOULD_SWITCH_TURN = False
                    config.switch_player_turn()
                self.check_collision()
                self.parent.dice.button.setEnabled(True)  # Re-enable dice for next player

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
        target_width = int(bg_width * scale_factor)
        target_height = int(bg_height * scale_factor)

        path = os.path.join(config.ASSETS_DIR, "Pawns", f"pawn_{self.color}.png")
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.button.setIcon(QIcon(scaled))
            self.button.setIconSize(scaled.size())
            self.button.resize(scaled.size())

        btn_width = self.button.width()
        btn_height = self.button.height()
        x = int(label.x() + (rel_x + 0.025) * bg_width - btn_width / 2)
        y = int(label.y() + (rel_y + 0.025) * bg_height - btn_height / 2)

        x = max(0, min(x, self.parent.width() - btn_width))
        y = max(0, min(y, self.parent.height() - btn_height))

        self.button.move(x, y)



    def check_collision(self):
        for pawn in self.parent.pawns:
            if pawn is self:
                continue
            if pawn.current_pos == self.current_pos and pawn.color != self.color:
                if not self.parent.is_safe_zone(self.current_pos):
                    self.cut_pawn(pawn)
                    break


    def cut_pawn(self, pawn):
        print(f"✂️ {self.color} pawn cut {pawn.color} pawn at {self.current_pos}")
        pawn.current_pos = pawn.pawn_id
        pawn.update_position()
        # award extra turn:
        config.SHOULD_SWITCH_TURN = False



