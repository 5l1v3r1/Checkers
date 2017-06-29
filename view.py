"""
-Редактор поля
-Отмена хода
-Лог игры
"""

import sys
from checkers import Game
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize


class View(QWidget):
    def __init__(self, game):
        super().__init__()
        
        #All game logig is inside class Game()
        self.game = game
        self.initUI()

    def initUI(self):
        #Textures
        self.w_imgs = (QPixmap("images\\w.png"), QPixmap("images\\w_q.png"))
        self.b_imgs = (QPixmap("images\\b.png"), QPixmap("images\\b_q.png"))

        #Update painter animation
        updater = QTimer(self)
        updater.start(150)
        updater.timeout.connect(self.update)

        #Window size
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))
        self.setWindowTitle('Checkers')

        #Start button
        startBtn = QPushButton("Start")
        startBtn.clicked.connect(self.game.start)

        #Radio buttons
        whiteBtn = QRadioButton("White")
        whiteBtn.setChecked(True)
        blackBtn = QRadioButton("Black")
        blackBtn.toggled.connect(self.game.setPlayer)
        
        difficultySpin = QSpinBox()
        difficultySpin.setMinimum(1)
        difficultySpin.setMaximum(15)
        difficultySpin.valueChanged.connect(self.game.setAiDepth)

        self.turnStatus = QLabel("Turn: White")
        
        #Place buttons on screen
        vbox = QVBoxLayout()
        vbox.addWidget(startBtn)
        vbox.addWidget(whiteBtn)
        vbox.addWidget(blackBtn)
        vbox.addWidget(QLabel("\nDiffuculty:"))
        vbox.addWidget(difficultySpin)
        vbox.addStretch(1)
        vbox.addWidget(self.turnStatus)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        #Show form
        self.setLayout(hbox)
        self.show()

    def paintEvent(self, e):
        """Paint board due to self.game.board"""

        #Update turn status
        strStatus = "White" if self.game.current_player == ("w", "W") else "Black"
        self.turnStatus.setText("Turn: " + strStatus)

        #Draw board 
        qp = QPainter()
        qp.begin(self)
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 1:
                    qp.setBrush(QColor(40, 41, 35))
                else:
                    qp.setBrush(QColor(255, 239, 219))
                qp.drawRect(j*50, i*50, 50, 50)
        
        #Draw figures
        board = self.game.board
        for i in range(8):
            for j in range(8):
                if board[i][j] == "w":
                    qp.drawPixmap(j*50+5, i*50+5, 40, 40, self.w_imgs[0])
                elif board[i][j] == "b":
                    qp.drawPixmap(j*50+5, i*50+5, 40, 40, self.b_imgs[0])
                elif board[i][j] == "W":
                    qp.drawPixmap(j*50+5, i*50+5, 40, 40, self.w_imgs[1])
                elif board[i][j] == "B":
                    qp.drawPixmap(j*50+5, i*50+5, 40, 40, self.b_imgs[1])
        qp.end()

    def getIandJ(self, e):
        """Get correct i and j from mouseEvent"""

        realPos = e.pos()
        x, y = realPos.x(), realPos.y()
        i, j = y // 50, x // 50

        #Mouse should be on board
        if not (0 < x < 400  and 0 < y < 400):
            return None, None

        return i, j

    def mousePressEvent(self, e):
        """Initialize self.game.last with i and j under cursor"""
        i, j = self.getIandJ(e)
        if (i, j) == (None, None):
            return

        board = self.game.board
        player = self.game.player
        
        if board[i][j] not in player:
            return

        self.game.last = (i, j)

    def mouseReleaseEvent(self, e):
        """Make move from self.game.last to new i and j"""
        last = self.game.last

        if last == (None, None):
            return

        i, j = self.getIandJ(e)
        if (i, j) == (None, None):
            return

        self.game.makeMove(last[0], last[1], i, j)
   

app = QApplication(sys.argv)
game = Game()
view = View(game)
sys.exit(app.exec_())