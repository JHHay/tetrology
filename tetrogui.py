# tetrogui.py

from graphics import *
from button import Button
from tetrobutton import TetroButton
from tetroinfo import InfoScreen

class GraphicsInterface:
    def __init__(self):
        self.winline = False

        # window
        self.x = 800
        self.y = 600
        
        self.win = GraphWin("Tetrology", self.x, self.y)
        self.win.setCoords(0,0,self.x,self.y)
        self.win.setBackground("black")

        self.makeHeader()
        
        self.status = self.splash()
        if self.status != "Quit":
            self.panel = ControlPanel(self.win, self.x, self.y,
                                      self.p1Name, self.p2Name)

            self.drawBoard(self.x,self.y)

    def makeHeader(self):
        header = Text(Point(self.x*.5, self.y*.975), "tetrology")
        header.setFill("yellow")
        header.setSize(16)
        header.draw(self.win)

        border = Line(Point(0,self.y*.95), Point(self.x,self.y*.95))
        border.setWidth(2)
        border.setFill("yellow")
        border.draw(self.win)

    def splash(self):
        splash = "tetrology - n. A version of Connect Four for the truly smooth."
        self.splashText = Text(Point(self.x*.5, self.y*.8), splash)
        self.splashText.setSize(20)
        self.splashText.setFill("yellow")
        self.splashText.draw(self.win)

        self.p1name = Text(Point(self.x*.2, self.y*.5), "Player 1 Name:")
        self.p1name.setFill("yellow")
        self.p1name.draw(self.win)

        self.p2name = Text(Point(self.x*.2, self.y*.4), "Player 2 Name:")
        self.p2name.setFill("yellow")
        self.p2name.draw(self.win)

        self.p1entry = Entry(Point(self.x*.5, self.y*.5), 15)
        self.p1entry.setText("Player 1")
        self.p1entry.draw(self.win)

        self.p2entry = Entry(Point(self.x*.5, self.y*.4), 15)
        self.p2entry.setText("Player 2")
        self.p2entry.draw(self.win)

        sButton = Button(self.win, Point(self.x*.5, self.y*.3), self.x*.2,
                         self.y*.05, "Start Game")
        sButton.activate()
        iButton = Button(self.win, Point(self.x*.5, self.y*.25), self.x*.2,
                         self.y*.05, "Info")
        iButton.activate()
        qButton = Button(self.win, Point(self.x*.5, self.y*.2), self.x*.2,
                         self.y*.05, "Quit")
        qButton.activate()
        while True:
            p = self.win.getMouse()
            p1name = self.p1entry.getText()
            p2name = self.p2entry.getText()
            if sButton.clicked(p):
                self.p1Name = self.p1entry.getText()
                self.p2Name = self.p2entry.getText()
                self.splashText.undraw()
                self.p1name.undraw()
                self.p2name.undraw()
                self.p1entry.undraw()
                self.p2entry.undraw()
                sButton.undraw()
                iButton.undraw()
                qButton.undraw()
                return "Play"
            elif iButton.clicked(p):
                iScreen = InfoScreen()
            elif qButton.clicked(p):
                return "Quit"

    def getNames(self):
        return self.p1Name, self.p2Name

    def getStatus(self):
        return self.status

    def choose(self, options):
        buttons = self.panel.buttons + self.board.tButtons
        for b in buttons:
            if b.getLabel() in options:
                b.activate()
            else:
                b.deactivate()
        while True:
            p = self.win.getMouse()
            for b in buttons:
                if b.clicked(p):
                    if b.getLabel() == "Info":
                        iScreen = InfoScreen()
                    else:
                        return b.getLabel()

    def drawBoard(self, x, y):
        self.board = PlayingBoard(self.win,x,y)

    def drawPiece(self, color, location):
        self.board.slots[location].setColor(color)

    def resetBoard(self):
        if self.winline:
            self.winLine.undraw()
        for slot in self.board.slots:
            self.board.slots[slot].setColor("black")

    def updateTurn(self, name, color):
        self.panel.marq.setText("{0}'s turn.".format(name))
        self.panel.marq.setFill(color)

    def displayWinner(self, name):
        self.panel.marq.setText("{0} wins! Play again?".format(name))

    def displayDraw(self):
        self.panel.marq.setText("A draw. Play again?")

    def updateScore(self, number, name, score):
        if number == 1:
            self.panel.p1Score.setText("{0:<12}:{1:>5}".format(name, score))
        if number == 2:
            self.panel.p2Score.setText("{0:<12}:{1:>5}".format(name, score))

    def drawLine(self, slotlist, color):
        loc1 = slotlist[0]
        loc2 = slotlist[-1]
        p1 = self.board.slots[loc1].getCenter()
        p2 = self.board.slots[loc2].getCenter()
        self.winLine = Line(p1,p2)
        self.winLine.setFill(color)
        self.winLine.setWidth(5)
        self.winLine.draw(self.win)
        self.winline = True

    def close(self):
        self.win.close()

class ControlPanel:
    def __init__(self, win, x, y, p1name, p2name):
        self.win = win

        # define boundaries
        
        self.x = x
        self.y = y*.25
                                 
        # draw background squares

        marqBG = Rectangle(Point(0,0), Point(self.x*.6, self.y))
        marqBG.setFill("slategray")
        marqBG.setWidth(2)
        marqBG.draw(win)

        scoreBG = Rectangle(Point(self.x*.6,0), Point(self.x*.9,self.y))
        scoreBG.setFill("slategray")
        scoreBG.setWidth(2)
        scoreBG.draw(win)

        buttonBG = Rectangle(Point(self.x*.9,0), Point(self.x,self.y))
        buttonBG.setFill("slategray")
        buttonBG.setWidth(2)
        buttonBG.draw(win)

        # create message marquee

        self.marq = Text(Point(self.x*.3, self.y*.5), "Hit 'Play' to begin.")
        self.marq.setSize(26)
        self.marq.setFill("yellow")
        self.marq.setStyle("bold")
        self.marq.draw(win)

        # create scoreboard text
        
        self.pString = "{0:<12}:{1:>5}"

        scoreTitle = Text(Point(self.x*.75, self.y*.85), "Games Won")
        scoreTitle.setFill("yellow")
        scoreTitle.setStyle("bold")
        scoreTitle.setSize(18)
        scoreTitle.draw(win)

        self.p1Score = Text(Point(self.x*.75,self.y*.6), self.pString.format(
            p1name, 0))
        self.p1Score.setSize(12)
        self.p1Score.setFill("yellow")
        self.p1Score.setFace("courier")
        self.p1Score.setStyle("bold")
        self.p1Score.draw(win)

        self.p2Score = Text(Point(self.x*.75,self.y*.3), self.pString.format(
            p2name, 0))
        self.p2Score.setSize(12)
        self.p2Score.setFill("yellow")
        self.p2Score.setFace("courier")
        self.p2Score.setStyle("bold")
        self.p2Score.draw(win)

        # create buttons
        self.buttons = []
        b = Button(win, Point(self.x*.95, self.y*.7),
                   self.x*.08, self.y*.2,
                   "Play")
        self.buttons.append(b)
        b = Button(win, Point(self.x*.95, self.y*.5),
                   self.x*.08, self.y*.2,
                   "Info")
        self.buttons.append(b)
        b = Button(win, Point(self.x*.95, self.y*.3),
                   self.x*.08, self.y*.2,
                   "Quit")
        self.buttons.append(b)

class PlayingBoard:
    def __init__(self, win, x, y):
        self.win = win
        self.x = x
        self.y = y
        self.xMin = x*.2
        self.xMax = x*.8
        self.yMin = y*.3
        self.yMax = y*.85
        self.colSpacing = (self.xMax - self.xMin) / 7
        self.rowSpacing = (self.yMax - self.yMin) / 6
        self.colCen = self.colSpacing / 2
        self.rowCen = self.rowSpacing / 2
        self.xC = self.xMin + ((self.xMax - self.xMin)/2)
        self.yC = self.yMin + ((self.yMax - self.yMin)/2)
        self.center = Point(self.xC, self.yC)

        self.scaffold = Rectangle(Point(self.xMin, self.yMin),
                                  Point(self.xMax, self.yMax))
        self.scaffold.setFill("green3")
        self.scaffold.draw(win)

        # make play buttons
        self.makeTButtons()

        # draw slots
        self.slots = {}
        for i in range(7):
            for j in range(6):
                self.slots[(i,j)] = Slot(win,
                                    Point(self.xMin + self.colCen + self.colSpacing * (i),
                                          self.yMin + self.rowCen + self.rowSpacing * (j)),
                                         self.colSpacing*.3)

    def makeTButtons(self):
        self.tButtons = []
        t = TetroButton(self.win, Point(self.xMin + self.colCen,
                                        self.yMax*1.06),
                        self.colSpacing * .8, "T0")
        self.tButtons.append(t)
        
        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing, self.yMax*1.06),
                        self.colSpacing * .8, "T1")
        self.tButtons.append(t)

        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing*2, self.yMax*1.06),
                        self.colSpacing * .8, "T2")
        self.tButtons.append(t)

        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing*3, self.yMax*1.06),
                        self.colSpacing * .8, "T3")
        self.tButtons.append(t)

        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing*4, self.yMax*1.06),
                        self.colSpacing * .8, "T4")
        self.tButtons.append(t)

        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing*5, self.yMax*1.06),
                        self.colSpacing * .8, "T5")
        self.tButtons.append(t)

        t = TetroButton(self.win, Point(self.xMin + self.colCen +
                                        self.colSpacing*6, self.yMax*1.06),
                        self.colSpacing * .8, "T6")
        self.tButtons.append(t)
                
class Slot:
    def __init__(self, win, center, radius):
        self.center = center
        self.radius = radius
        self.win = win
        self.visual = Circle(self.center, self.radius)
        self.visual.setFill("black")
        self.visual.draw(win)

    def setColor(self, color):
        self.visual.setFill(color)

    def getCenter(self):
        return self.center
