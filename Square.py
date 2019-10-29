class Square:
    def __init__(self,  value):
        self.value = value
        self.permanence = False
        self.black = False
        self.number = None


    def makeBlack(self):
        self.black = True
        self.permanence = True

    def getValue(self):
        if self.black:
            raise ValueError("this is a black square")
        return self.value

    def setValue(self, value, permanence):
        if self.black:
            raise ValueError("you can't put a letter in a black square")
        if permanence:
            self.permanence = permanence
        self.value = value

    def getNumber(self):
        return self.number

    def setNumber(self, num):
        if self.black:
            raise ValueError("you can't number a black square")
        self.number = num

    def isClueSquare(self):
        if self.number:
            return True
        return False

    def isBlack(self):
        return self.black

    def isPermanent(self):
        return self.permanence