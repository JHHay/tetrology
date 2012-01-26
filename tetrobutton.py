# tetrobutton.py

from graphics import *

class TetroButton:

    def __init__(self, win, center, width, label):
        self.win = win
        height = width * .25
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        p3 = Point(x-height,self.ymax)
        p4 = Point(x+height,self.ymax)
        p5 = Point(x, self.ymin)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill("green3")
        self.tri = Polygon(p3,p4,p5)
        self.tri.setFill("white")
        self.active = False
        self.label = label

    def clicked(self, p):
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        return self.label   

    def activate(self):
        if self.active == False:
            self.rect.draw(self.win)
            self.tri.draw(self.win)
            self.active = True

    def deactivate(self):
        self.rect.undraw()
        self.tri.undraw()
        self.active = False
