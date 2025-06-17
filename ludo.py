import sys
import random
import os
from pygame import mixer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.final_dice_roll = 1  # Initialize final dice roll value
        self.shuffle_count = 0
        self.max_shuffle = 6
        self.target_position = 1   # Will be updated after dice roll
        self.current_position = 1  # Pawn starts at position 1

        roll = random.randint(1, 6)
        dice_path = os.path.join("Assets", "Dice_Outcomes", f"dice{roll}.png")
        
        # *** BLUE PAWN COORDINATES ***
        self.coordinates = [
            (1, 0.7, 0.7),
            (2, 0.85, 0.54),
            (3, 0.79, 0.54),
            (4, 0.725, 0.54),
            (5, 0.6625, 0.54),
            (6, 0.6, 0.54),
            (7, 0.537, 0.605),
            (8, 0.537, 0.670),
            (9, 0.537, 0.735),
            (10, 0.537, 0.8),
            (11, 0.537, 0.865),
            (12, 0.537, 0.929), 
            (13, 0.477, 0.929),
            (14, 0.412, 0.929),
            (15, 0.412, 0.865),
            (16, 0.412, 0.8),
            (17, 0.412, 0.735),
            (18, 0.412, 0.670),
            (19, 0.412, 0.605),
            (20, 0.352, 0.54)
        ]

        self.setWindowTitle("Ludo Game")
        self.setGeometry(100, 100, 800, 600)  # Initial window size
        self.setStyleSheet("background: white;")  # Make window background transparent

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width(), self.height()-30)
        self.label.setAlignment(Qt.AlignCenter)
        self.set_background_image()

        # *** VARS AND TIMERS RELATED TO DICE SHUFFLING ***
        self.timer = QTimer()
        self.timer.timeout.connect(self.shuffle_dice)

        # *** VARS AND TIMERS RELATED TO PAWN MOVEMENT ***
        self.movement_timer = QTimer()
        self.movement_timer.timeout.connect(self.move_pawn_step)

        # *** PAWN IMAGE & BUTTONS ***
        self.pawn_path = os.path.join("Assets", "Pawns", "pawn_blue.png")
        self.pawn_button = QPushButton(self)  # Create the pawn button as an instance variable
        self.load_pawn_image()  # Load pawn image when the window is created
        
        # *** CREATING A DICE BUTTON ***
        i = random.randint(1, 6)
        dice_path = os.path.join("Assets", "Dice_Outcomes", f"dice{i}.png")
        self.DiceButton = QPushButton(self)
        self.DiceButton.setIcon(QIcon(dice_path))
        self.DiceButton.setGeometry(200, 200, 75, 75)
        self.DiceButton.setIconSize(self.DiceButton.size()) 
        self.DiceButton.clicked.connect(self.on_dice_click)
        self.set_DiceButton_position()

    def load_pawn_image(self):
        pawn = QPixmap(self.pawn_path)
        if pawn.isNull():
            print("Error: Unable to load the image.")
        else:
            print("Image loaded successfully!")
            pawn_icon = QIcon(pawn)  # Convert QPixmap to QIcon
            self.pawn_button.setIcon(pawn_icon)  # Set the QIcon as the button's icon
            self.pawn_button.setFlat(True)
            self.pawn_button.setStyleSheet("background-color: rgba(0,0,0,0); border: none;")
            self.pawn_button.resize(50, 50)  # Default size, will be adjusted in `update_pawn_position`
            self.label.lower()  # Make sure the pawn button is lower than the background image
            self.update_pawn_position()  # Update the initial position

    def resizeEvent(self, event):
        # Update the size of the background Ludo board when resizing window
        self.set_background_image()

        # Update the size and position of the pawn image button when resizing the window
        self.update_pawn_position()

        super().resizeEvent(event)

        # Update the size of the dice button when resizing the window
        self.set_DiceButton_position()

    def set_background_image(self):
        """Set and scale the background image to cover the entire window."""
        pixmap = QPixmap("Assets/ludoboard.jpg")
        self.board_width = pixmap.width()
        self.board_height = pixmap.height()

        if pixmap.isNull():
            print("Failed to load image")
            return

        scaled_pixmap = pixmap.scaled(self.width(), self.height() - 50, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.label.setGeometry(0, 0, self.width(), self.height() - 75)

    def set_DiceButton_position(self):
        """Set the position of the button at the bottom center."""
        button_width = self.DiceButton.width()
        button_height = self.DiceButton.height()
        x = (self.width() - button_width) // 2
        y = self.height() - button_height - 3
        self.DiceButton.move(x, y)

    def on_dice_click(self):
        mixer.init()
        dice_rolling_sound = mixer.Sound("Assets/Sounds/Dice_Rolling.mp3")
        dice_rolling_sound.play()
        dice_rolling_sound.set_volume(0.2)

        self.shuffle_count = 0
        self.timer.start(50)  # Shuffle every 50 ms


    def shuffle_dice(self):
        if self.shuffle_count < self.max_shuffle - 1:
            temp_roll = random.randint(1, 6)
            dice_path = os.path.join("Assets", "Dice_Outcomes", f"dice{temp_roll}.png")
            self.DiceButton.setIcon(QIcon(dice_path))
            self.DiceButton.setIconSize(self.DiceButton.size())
            self.shuffle_count += 1

        else:
            # Final roll
            self.final_dice_roll = random.randint(1, 6)
            dice_path = os.path.join("Assets", "Dice_Outcomes", f"dice{self.final_dice_roll}.png")
            self.DiceButton.setIcon(QIcon(dice_path))
            self.DiceButton.setIconSize(self.DiceButton.size())
            self.timer.stop()
            self.start_pawn_movement()  # START MOVEMENT AFTER final roll


    def start_pawn_movement(self):
        print(f"Final Dice Rolled: {self.final_dice_roll}")

        self.target_position = self.current_position + self.final_dice_roll

        # Cap target to last valid coordinate
        if self.target_position > len(self.coordinates):
            self.target_position = len(self.coordinates)

        self.movement_timer.start(100)

    def update_single_pawn_position(self):
        pos, rel_x, rel_y = self.coordinates[self.current_position - 1]  # -1 because list is 0-indexed

        bg_x = self.label.x()
        bg_y = self.label.y()
        bg_width = self.label.width()
        bg_height = self.label.height()

        scale_factor = 0.05
        pawn_width = int(bg_width * scale_factor)
        pawn_height = int(bg_height * scale_factor)

        new_x = int(bg_x + rel_x * bg_width)
        new_y = int(bg_y + rel_y * bg_height)

        self.pawn_button.move(new_x, new_y)
        self.pawn_button.resize(pawn_width, pawn_height)

        pixmap = QPixmap(self.pawn_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(pawn_width, pawn_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.pawn_button.setIcon(QIcon(scaled_pixmap))
            self.pawn_button.setIconSize(self.pawn_button.size())

    def update_pawn_position(self):
        self.update_single_pawn_position()

    def move_pawn_step(self):
        if self.current_position < self.target_position:
            self.current_position += 1
            self.update_single_pawn_position()
        else:
            self.movement_timer.stop()

    def get_coordinates(self):
        # Get current absolute position of the pawn button
        pawn_x = self.pawn_button.x()
        pawn_y = self.pawn_button.y()
        print(f"Absolute Position: x={pawn_x}, y={pawn_y}")

        # Get relative position with respect to the background label
        bg_x = self.label.x()
        bg_y = self.label.y()
        bg_width = self.label.width()
        bg_height = self.label.height()

        # Compute relative coordinates (as a percentage of the background)
        rel_x = (pawn_x - bg_x) / bg_width
        rel_y = (pawn_y - bg_y) / bg_height
        print(f"Relative Position (percent): x={rel_x:.3f}, y={rel_y:.3f}")

    def pawn_button_clicked(self):
        self.get_coordinates()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
