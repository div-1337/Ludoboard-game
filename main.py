# Developed by div-1337
#
# HELP TAKEN FROM CHATGPT ASWELL FOR FRONT END AND PAWN MOVING DYNAMICS, FRONT END LUDOBOARD PLACEMENT, PAWN CUTTING
#
#
# DEVELOPED FOR EDUCATIONAL PURPOSE
#
#

from PyQt5.QtWidgets import QApplication
import sys
from game.board import GameWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
