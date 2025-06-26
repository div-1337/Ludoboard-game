from PyQt5.QtWidgets import QApplication
import sys
from game.board import GameWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
