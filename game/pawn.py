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
        self.coords = coords
        self.current_pos = pawn_id
        self.target_pos = pawn_id

        self.button = QPushButton(parent)
        self.button.setFlat(True)
        self.button.setStyleSheet("background-color: rgba(0,0,0,0); border: none;")
        self.button.resize(50, 50)
        self.load_image()

        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.step_move)

        self.button.clicked.connect(self.on_click)
        self.update_position()

    def on_click(self):
        if config.DICE_FINAL_VALUE is None:
            print("⚠️ Dice has not been rolled yet!")
            return

        print(f"on_click called for pawn {self.pawn_id} with dice value {config.DICE_FINAL_VALUE}")

        if config.DICE_ROLLED == 1 and not self.timer.isActive():
            allowed_ids = config.PLAYER_PAWNS[config.CURRENT_PLAYER]
            if self.pawn_id not in allowed_ids:
                print(f"❌ Not your turn — pawn {self.pawn_id} is inactive.")
                return

            if self.current_pos < 0 and config.DICE_FINAL_VALUE not in (1, 6):
                print(f"❌ Invalid move: Pawn is in base and dice is {config.DICE_FINAL_VALUE}")
                return

            print(f"Starting move for {self.pawn_id}")
            success = self.move_to(config.DICE_FINAL_VALUE)
            if success:
                self.timer.start(100)
            else:
                print("🚫 Invalid move. Checking if any other pawn can move...")

                other_pawns = [p for p in self.parent.pawns if p.pawn_id in allowed_ids and p is not self]
                can_any_move = any(p.move_to_simulation(config.DICE_FINAL_VALUE) for p in other_pawns)

                if not can_any_move:
                    print(f"🚫 {config.CURRENT_PLAYER.capitalize()} has no valid moves — skipping turn.")
                    config.SHOULD_SWITCH_TURN = True
                    config.DICE_FINAL_VALUE = None
                    config.DICE_ROLLED = 0
                    config.switch_player_turn()
                    self.parent.dice.button.setEnabled(True)
        else:
            print("❌ Dice not rolled, already moved, or pawn is moving.")

    def move_to(self, steps):
        print(f"move_to called with steps={steps}")

        if self.current_pos < 0 and steps in (1, 6):
            start_positions = {"blue": 0, "red": 13, "green": 26, "yellow": 39}
            self.target_pos = start_positions.get(self.color)
            print(f"🎯 Moving from base to starting position: {self.target_pos}")
            self.current_pos = self.target_pos
            self.update_position()
            config.DICE_ROLLED = 0
            config.DICE_FINAL_VALUE = 0
            config.SHOULD_SWITCH_TURN = True
            self.parent.dice.button.setEnabled(True)
            config.switch_player_turn()
            return False

        sorted_positions = sorted(k for k in self.coords if k >= 0)
        if self.current_pos not in sorted_positions:
            print(f"⚠️ current_pos {self.current_pos} not in coords keys")
            return False

        current_index = sorted_positions.index(self.current_pos)
        target_index = current_index + steps

        entry_index = config.ENTRY_INDEX[self.color]
        finish_path = {
            "blue": config.BLUE_FINISH,
            "red": config.RED_FINISH,
            "green": config.GREEN_FINISH,
            "yellow": config.YELLOW_FINISH
        }[self.color]

        if self.current_pos in finish_path:
            i = finish_path.index(self.current_pos)
            new_index = i + steps
            if new_index < len(finish_path):
                self.target_pos = finish_path[new_index]
                return True
            else:
                print("⛔ Move too far — cannot go past final finish square.")
                return False
        elif current_index < entry_index <= target_index:
            offset = target_index - (entry_index + 1)
            if offset < len(finish_path):
                self.target_pos = finish_path[offset]
                return True
            else:
                print("⛔ Move too long — exceeds finish path entry.")
                return False
        else:
            if self.color in ("red", "green", "yellow"):
                target_index %= config.MAX_POSITIONS
            if target_index >= len(sorted_positions):
                print("⛔ Target index out of range.")
                return False
            self.target_pos = sorted_positions[target_index]
            return True

    def step_move(self):
        print(f"[step_move] current_pos: {self.current_pos}, target_pos: {self.target_pos}")

        finish_path = {
            "blue": config.BLUE_FINISH,
            "red": config.RED_FINISH,
            "green": config.GREEN_FINISH,
            "yellow": config.YELLOW_FINISH
        }[self.color]

        if self.current_pos == self.target_pos:
            self.timer.stop()

            reached_finish = self.current_pos == config.final_finish_ids[self.color]
            if reached_finish:
                placed = self.move_to_exit_zone()
                if placed:
                    config.SHOULD_SWITCH_TURN = False
                else:
                    config.SHOULD_SWITCH_TURN = True

            self.check_collision()
            self.parent.dice.button.setEnabled(True)

            config.DICE_ROLLED = 0
            config.DICE_FINAL_VALUE = 0

            if config.SHOULD_SWITCH_TURN:
                config.SHOULD_SWITCH_TURN = False
                config.switch_player_turn()

            return

        if self.current_pos in finish_path:
            idx = finish_path.index(self.current_pos)
            if idx + 1 < len(finish_path):
                self.current_pos = finish_path[idx + 1]
            else:
                self.timer.stop()
                print("⚠️ Already at the end of finish path.")
        elif self.current_pos == config.ENTRY_INDEX[self.color]:
            self.current_pos = finish_path[0]
        else:
            self.current_pos = (self.current_pos + 1) % config.MAX_POSITIONS

        self.update_position()

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




        if config.CURRENT_PLAYER == self.color:
            self.button.setStyleSheet("border: 15px solid white; border-radius: 5px; background-color: rgba(0,0,0,0);")
        else:
            self.button.setStyleSheet("border: none; background-color: rgba(0,0,0,0);")




        
        if self.current_pos in config.PAWN_COORDINATES:
            rel_x, rel_y = config.PAWN_COORDINATES[self.current_pos][:2]
        elif self.current_pos in config.BOARD_EXIT_ZONE:
            rel_x, rel_y, _ = config.BOARD_EXIT_ZONE[self.current_pos]
        else:
            print(f"⚠️ Invalid position: {self.current_pos}")
            return

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

        x = int(label.x() + (rel_x + 0.025) * bg_width - self.button.width() / 2)
        y = int(label.y() + (rel_y + 0.025) * bg_height - self.button.height() / 2)
        self.button.move(max(0, min(x, self.parent.width())), max(0, min(y, self.parent.height())))

    def check_collision(self):
        for pawn in self.parent.pawns:
            if pawn is self:
                continue
            if pawn.current_pos == self.current_pos and pawn.color != self.color:
                if not self.parent.is_safe_zone(self.current_pos):
                    self.cut_pawn(pawn)
                    return

    def cut_pawn(self, pawn):
        print(f"✂️ {self.color} pawn cut {pawn.color} pawn at {self.current_pos}")
        pawn.current_pos = pawn.pawn_id
        pawn.update_position()
        # No turn switch here if you want to give extra turn on cut
        config.SHOULD_SWITCH_TURN = False

    def move_to_exit_zone(self):
        start_id = {
            "blue": 116, "red": 216, "green": 316, "yellow": 416
        }[self.color]

        print(f"🔍 Trying to move {self.color} pawn to exit zone...")
        for i in range(4):
            exit_id = start_id + i
            x, y, z = config.BOARD_EXIT_ZONE.get(exit_id, (None, None, 1))
            print(f"Checking exit_id {exit_id}: occupied={z}")
            if z == 0:
                config.BOARD_EXIT_ZONE[exit_id] = (x, y, 1)
                self.current_pos = exit_id
                self.button.setEnabled(False)
                self.button.setStyleSheet("border: none; background-color: rgba(0, 0, 0, 0);")
                self.update_position()
                print(f"🏁 {self.color.capitalize()} pawn moved to exit zone at {exit_id}")
                config.PLAYER_FINISH_COUNT[self.color] += 1
                if config.PLAYER_FINISH_COUNT[self.color] == 4:
                    print(f"🏆 {self.color.upper()} has won the game!")
                return True
        print(f"❌ No space in exit zone for {self.color} pawn!")
        return False

    def move_to_simulation(self, steps):
        if self.current_pos < 0:
            return steps in (1, 6)

        finish_path = {
            "blue": config.BLUE_FINISH,
            "red": config.RED_FINISH,
            "green": config.GREEN_FINISH,
            "yellow": config.YELLOW_FINISH
        }[self.color]

        if self.current_pos in finish_path:
            i = finish_path.index(self.current_pos)
            return (i + steps) < len(finish_path)

        sorted_positions = sorted(k for k in self.coords if k >= 0)
        if self.current_pos not in sorted_positions:
            return False

        current_index = sorted_positions.index(self.current_pos)
        target_index = current_index + steps

        if self.color in ("red", "green", "yellow"):
            target_index %= config.MAX_POSITIONS

        return target_index < len(sorted_positions)
    

    def highlight(self, enabled=True):
        if enabled:
            self.button.setStyleSheet("border: 3px solid white; background-color: rgba(0,0,0,0);")
        else:
            self.button.setStyleSheet("border: none; background-color: rgba(0,0,0,0);")