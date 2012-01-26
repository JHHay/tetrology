# tetrology.py

from tetrogui import GraphicsInterface
from tetroboard import PlayingBoard
from tetroinfo import InfoScreen


class TetrologyApp:
    def __init__(self):
        """Turns game on, loads graphics, sets player colors, loads playing board, creates players and playing order"""

        self.playing = True
        self.interface = GraphicsInterface()
        p1name, p2name = self.interface.getNames()
        p1color = "tan"
        p2color = "yellow"

        self.board = PlayingBoard()

        self.player1 = Player(p1name, 1, p1color)
        self.player2 = Player(p2name, 2, p2color)

        goesFirst = self.player1

    def run(self):
        """The main game loop"""

        if self.interface.getStatus != "Quit":
            goesFirst = self.player1
            while self.playing:
                self.choice = "init"
                self.choice = self.interface.choose(["Play", "Info", "Quit"])
                self.interface.resetBoard()
                self.board.reset()
                self.action("None")

                if self.playing:
                    self.interface.resetBoard()
                    self.board.reset()
                    winner = self.playRound(goesFirst)

                if self.playing:
                    goesFirst = self.endGame(winner, goesFirst)

    def playRound(self, goesFirst):
        """A round of play."""
        self.gameOver = 0
        activePlayer = goesFirst
        self.interface.updateTurn(activePlayer.getName(),
                                  activePlayer.getColor())
        tButtonList = self.board.openColumns() 
        self.choice = self.interface.choose(["Info", "Quit"] + tButtonList)
        self.action(activePlayer)
        while self.playing and not self.gameOver:
            self.checkWin()

            if self.playing and not self.gameOver:
                activePlayer = self.changePlayer(activePlayer)
                self.interface.updateTurn(activePlayer.getName(),
                                          activePlayer.getColor())
                tButtonList = self.board.openColumns()
                self.choice = self.interface.choose(["Info", "Quit"]
                                                        + tButtonList)
                self.action(activePlayer)

        if self.gameOver:

            if self.result == "Win":
                return activePlayer
            elif self.result == "Draw":
                return "Nobody"

    def checkWin(self):
        status = self.board.checkStatus()

        if status == "tetra":
            self.gameOver = True
            self.result = "Win"

        if status == "full":
            self.gameOver = True
            self.result = "Draw"

    def changePlayer(self, activeplayer):

        if activeplayer.getNumber() == 1:
            return self.player2

        else:
            return self.player1

    def endGame(self, winner, default):
        if winner == "Nobody":               # A tie
            self.interface.displayDraw()
            return default
        else:
            self.interface.drawLine(self.board.getWinPieces(),
                                    winner.getColor())
            self.interface.displayWinner(winner.getName())
            winner.addWin()
            self.interface.updateScore(winner.getNumber(),
                                       winner.getName(), winner.getWins())
            return winner
    

    def action(self, player):
        if self.choice == "Quit":
            self.playing = False
        if self.choice[0] == "T":
            self.addPiece(player, self.choice[1])

    def addPiece(self, player, column):
        location = self.board.addPiece(player.getNumber(), int(column))
        self.interface.drawPiece(player.getColor(), location)

    def close(self):                         # Cleaning up
        self.interface.close()

class Player:
    def __init__(self, name, number, color):
        self.name = name
        self.number = number
        self.color = color
        self.wins = 0

    def getName(self):
        return self.name

    def getNumber(self):
        return self.number

    def getColor(self):
        return self.color

    def getWins(self):
        return self.wins

    def addWin(self):
        self.wins = self.wins + 1

if __name__=="__main__":
    Tetrology = TetrologyApp()
    Tetrology.run()
    Tetrology.close()
