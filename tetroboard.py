# tetroboard.py

directions = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]

class PlayingBoard:
    def __init__(self):
        self.status = "open"
        self.columns = []
        self.winningpieces = [] # initializing list of winning pieces
        for i in range(7):
            c = Column(i)
            self.columns.append(c)
        
    def reset(self):
        # clears board
        for column in self.columns:
            column.empty()
    
    def openColumns(self):
        # returns a list of available columns
        opencolumns = []
        for column in self.columns:
            if column.checkOpen():
                opencolumns.append("T" + str(column.getLocation()))
        return opencolumns

    def checkStatus(self):
        if self.openColumns():
            return self.status
        else:
            return "full"
        
    def getWinPieces(self):
        self.winningpieces.sort()
        return self.winningpieces

    def addPiece(self, player, column):
        slot = self.columns[column].dropPiece(player)
        location = (column, slot)
        self.checkWin(location, player)
        return location

    def checkWin(self, location, player):
        # determines if the piece has entered a winning line
        # if so, adds the locations of the pieces to self.winningpieces
        # and sets self.status to "tetra"
        self.winningpieces.append(location)
        l = location
        for d in directions:
            x = d[0] + l[0]
            if 0 <= x < 7:
                y = d[1] + l[1]
                if 0 <= y < 6:
                    if self.columns[x].slots[y].checkOwner() == player:
                        self.winningpieces = []
                        self.winningpieces.append((x,y))
                        count = 3
                        count = self.linkSearch(x, y, d, player, count)
                        if count == 0:
                            self.status = "tetra"
                            return None
                        else:
                            reverse = self.reverseDirection(d)
                            count = self.linkSearch(x,y,reverse,player,count)                  
                            if count == 0:
                                self.status = "tetra"
                                return None
        self.status = "open"
         
                        
    def linkSearch(self, x, y, direction, player, count):
        if count == 0:
            return count
        else:
            dx, dy = x + direction[0], y + direction[1]
            if 0<= dx < 7 and 0<= dy < 6:
                if self.columns[dx].slots[dy].checkOwner() == player:
                    self.winningpieces.append((dx,dy))
                    count = self.linkSearch(dx, dy, direction, player, count - 1)
                    return count
                else:
                    return count
            else:
                return count
                        
    def reverseDirection(self, direction):
        x, y = direction[0]*-1, direction[1]*-1
        return (x,y)                        
        
class Column:
    def __init__(self, number):
        self.myLocation = number
        self.slots = []
        for i in range(6):
            r = Slot(i)
            self.slots.append(r)

    def empty(self):
        for slot in self.slots:
            slot.empty()

    def getLocation(self):
        return self.myLocation

    def checkOpen(self):
        for slot in self.slots:
            if slot.checkEmpty():
                return True
        return False

    def dropPiece(self, player):
        for slot in self.slots:
            if slot.checkEmpty():
                slot.fill(player)
                return slot.getLocation()
        

class Slot:
    def __init__(self, number):
        self.myLocation = number
        self.isEmpty = True
        self.owner = 0

    def empty(self):
        self.isEmpty = True
        self.owner = 0

    def checkEmpty(self):
        if self.isEmpty:
            return True
        else:
            return False
            
    def checkOwner(self):
        return self.owner

    def fill(self, player):
        self.isEmpty = False
        self.owner = player

    def getLocation(self):
        return self.myLocation

