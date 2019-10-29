def findRow(spot, w):
    return spot / w
def findCol(spot, w):
    return spot % w
def getRowAbove(spot):
    return spot - w
def getColBehind(spot):
    return spot - 1
def findClueSpots(string, h, w):
        clues = []
        counter = 1
        for spot in range(0, h * w):
            i = findRow(spot, w)
            j = findCol(spot, h)
            print(i, j)
            if string[spot] == "$":
                pass
            else:
                
                rowAbove = getRowAbove(spot)
                if i == 0 or string[rowAbove] == "$":
                    clues.append(("down", i - 1, j))
                    counter = self.numberItIfItsUnnumbered((i, j), counter)
                if j == 0 or self.isBlackSquare((i, j - 1)):
                    clues.append(("across", i, j))
                    counter = self.numberItIfItsUnnumbered((i, j), counter)
        return clues