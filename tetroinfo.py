# tetroinfo.py

from button import Button
from graphics import *

class InfoScreen:
    def __init__(self):
        win = GraphWin("tetrologyology", 400,400)
        win.setBackground("black")

        text = Text(Point(200, 50), "tetrology v0.1")
        text.setSize(18)
        text.setStyle("bold")
        text.setFill("yellow")
        text.draw(win)

        text2 = Text(Point(200, 150), "Joe Hay -- 2011")
        text2.setFill("yellow")
        text2.draw(win)

        ex = Button(win, Point(200, 300), 60, 25, "Exit")
        ex.activate()

        p = win.getMouse()
        while not ex.clicked(p):
            p = win.getMouse()

        win.close()

        
