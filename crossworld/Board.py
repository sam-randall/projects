# Sam Randall
# CrossWord Generator May 29, 2019
# coding: utf-8> 
import time
import random
import Trie
#import tkinter
import Square
import Board_helper


class Board:
    def __init__(self, height, width, empty_squares=None, compressedBoard = None):
        self.board = [[Square.Square("") for i in range(height)] for j in range(width)]
        self.height = height
        self.width = width
        if compressedBoard:
            for i in range(len(compressedBoard)):
                r = Board_helper.findRow(i, width)
                c = Board_helper.findCol(i, width)
                if compressedBoard[i] == '$':
                    self.setBlack((r, c))
                else:
                    self.assignCharacter((r, c), compressedBoard[i])
        else:
            for pair in empty_squares:
                self.setBlack(pair)
        self.clueDirAndStart = self.findClueSpots()

        # regardless of across or down. 
        self.clueSpots = []
        self.numOfClues = {}
        prev = (None, None)
        counter = 1
        for clue in self.clueDirAndStart:
            direction, row, col = clue
            if  (row, col) != prev:
                self.clueSpots.append((row, col))
                self.numOfClues[(row, col)] = counter 
                counter += 1
            prev = (row, col)
        self.spacesOfWords = []
        for direction, row, col in self.clueDirAndStart:
            self.spacesOfWords.append(self.coordWord((row, col), direction))

    ''' fillInPuzzle autofills in a Board'''
    def fillInPuzzle(self, triesAltered, across, down, howManySimulations=1000,
     loopsToFindValidWord=50):
        words = []
        result = Board_helper.alternate(across, down)
        for direction, i, j in across: #unfilledAcross

            pair = (i, j)
            start = time.time()
            clueCoords, lengthOfClueWord = self.coordWord(pair, direction)
            info = self.wordInfo(clueCoords)
            orderOfTrie, allPermanent = self.orderOfTrie(clueCoords)
            trieOfInterest = triesAltered[(lengthOfClueWord, orderOfTrie)]
            # check what info we know and use it. to get right trie. 
            score = 0
            maxScore = 0
            bestWord = None
            howManyWords = trieOfInterest.getSize()
            if not allPermanent:
                constraints = self.findConstraintsOnNextWord(triesAltered, clueCoords, direction)
                if not constraints:
                    return False, False, words
                possible = Board_helper.howManyComboInListOfLists(constraints)
                newConstraints = Board_helper.putListIntoCustomizedOrder(constraints, orderOfTrie)

                maxScore, bestWord = self.simulateToFindBestWord(
                    howManySimulations, loopsToFindValidWord, trieOfInterest, triesAltered, pair,
                 clueCoords, newConstraints, direction, orderOfTrie, words)
                if Board_helper.noneFound(maxScore):
                    return False, False, words
                nextWord = Board_helper.putCustomizedOrderWordIntoEnglish(bestWord, orderOfTrie)
                self.assignWord(pair, direction, nextWord) 
                words.append(nextWord)
                triesAltered = Board_helper.removeWordFromAllRelevantTries(nextWord, triesAltered)
        acrossWords, downWords = self.getAcrossAndDown()        
        return acrossWords, downWords, words

    ''' returns list [(num, word) ...] for acrossWords, downWords'''
    def getAcrossAndDown(self):
        across = [(direction, row, col) for direction, row, col in self.clueDirAndStart if direction == "across"]
        down = [(direction, row, col) for direction, row, col in self.clueDirAndStart if direction == "down" ]
        acrossWords = []
        downWords = []
        for direction, i, j in across:
            pair = (i, j)
            coord, length = self.coordWord(pair, "across")
            acrossWords.append((self.getSquare(pair).getNumber(), self.wordInClue(coord)))
        for direction, i, j in down:
            pair = (i, j)
            coord, length = self.coordWord(pair, "down")
            downWords.append((self.getSquare(pair).getNumber(), self.wordInClue(coord)))
        return acrossWords, downWords

    '''helper function to initially form tries that we'll use'''
    '''explanation here is we need different information depending on our autofill info'''
    def _generateTriesByNeedOneDirection(self, clueSpots, ds, tries={}):
        for direction, row, col in clueSpots:
            pair = (row, col)
            wordCoordinates, length = self.coordWord(pair, direction)
            infoInTable = self.wordInfo(wordCoordinates)
            orderOfTrie, allPermanent = self.orderOfTrie(wordCoordinates)
            if (length, orderOfTrie) in tries:
                continue
            else:
                dictionaryOfWordOfRightLength = ds[length - 3]
                trieMadeTheRightWay = Trie.Trie(None)
                # TAKES A LOT OF TIME!
                for word in dictionaryOfWordOfRightLength:
                    wordAltered = Board_helper.putWordIntoCustomizedOrder(word, orderOfTrie)
                    trieMadeTheRightWay = trieMadeTheRightWay.addWord(wordAltered)
                tries[(length, orderOfTrie)] = trieMadeTheRightWay
        return tries

    '''see helper function, generate tries depending on what words we need to fill in'''
    def generateTriesByNeed(self, ds, across, down):
        tries = self._generateTriesByNeedOneDirection(across, ds)
        tries = self._generateTriesByNeedOneDirection(down, ds, tries)
        return tries

    '''as we simulate, function returns list of acceptable letters for each position in current clue'''
    def findConstraintsOnNextWord(self, tries, startCoordinates, clueDirection):
        constraints = [[] for i in range(len(startCoordinates))]
        words = []
        found = False
        for i, clue in enumerate(startCoordinates):
            valueInSquare = self.getSquare(clue).getValue()
            coordDown = self._findIntersectingClue(clue, clueDirection)
            wordCoordinates, length = self.coordWord(coordDown, Board_helper.oppositeDirection(clueDirection))
            info = self.wordInfo(wordCoordinates)
            order, allPermanent = self.orderOfTrie(wordCoordinates)
            trie = tries[(length, order)]
            prefix = Board_helper.determineAlteredPrefix(info, order)
            children = trie.getChildren(prefix) 
            if valueInSquare:
                found = True
                constraints[i] = [valueInSquare]
            elif not children:
                return False # I think we know it fucked up here if this turns out to be true!
            else:
                found = True
                constraints[i] = children
        return constraints

    '''run a simulation to find the highest score, most likely to lead to a success to place a word in selected location'''
    def simulateToFindBestWord(self, iterations, loopsMax, trie, tries, pair, coordinatesOfClue,
     constraints, direction, order, words):
        maxScore = 0
        bestWord = None
        for j in range(iterations):
            word = trie.getRandomWordGivenConstraints(constraints) # again update
            loops = 0
            while (not word or word in words) and loops < loopsMax:
                word = trie.getRandomWordGivenConstraints(constraints)
                loops += 1
            if not word or word in words:
                return 0, None
            self.assignWord(pair, direction, Board_helper.putCustomizedOrderWordIntoEnglish(word, order)) # need to apply function on word here
            score = self.findFrequencyScoreOfBeginnings(tries, coordinatesOfClue, direction) # consult the right tries
            if score > maxScore:
                maxScore = score
                bestWord = word
            self.clearWord(pair, direction, len(constraints))
        if Board_helper.noneFound(maxScore):
            return 0, bestWord
        return maxScore, bestWord

    '''helper for simulation, we want to return the minimum, (weakest link), frequency fro the prefixes places in the simulation'''
    def findFrequencyScoreOfBeginnings(self, tries, startCoordinates, clueDirection):
        # we're assuming all asigned words are inputted in the right order.
        minimumFreq = 999999
        for clue in startCoordinates:
            coordDown = self._findIntersectingClue(clue, clueDirection)
            wordCoordinates, length = self.coordWord(coordDown, Board_helper.oppositeDirection(clueDirection))

            #### NEED TO GET WORD INFO 
            info = self.wordInfo(wordCoordinates)
            orderOfTrie, allPermanent  = self.orderOfTrie(wordCoordinates) 
            trieOfInterest = tries[(length, orderOfTrie)]
            prefix = Board_helper.determineAlteredPrefix(info, orderOfTrie)

            if len(prefix) < length: 
                freq = trieOfInterest.frequencyOfPrefix(prefix)
                if freq == 0:
                    return 0
                elif freq < minimumFreq:
                    minimumFreq = freq
            elif len(prefix)== length:
                if trieOfInterest.doesWordExist(prefix):
                    continue
                elif allPermanent:
                    continue
                else:
                    return 0
        return minimumFreq
    ''' input: coordinates, output: word in clue.
    '''
    def wordInClue(self, coordinates):
        string = ""
        for pair in coordinates:
            string += self.getSquare(pair).getValue()
        return string
    ''' input coordinates: where do we know information'''
    def wordInfo(self, coordinates):
        string = ""
        for pair in coordinates:
            sq = self.getSquare(pair)
            val = sq.getValue()
            if val == "":
                string += '0'
            else:
                string += val
        return string

    def orderOfTrie(self, coordinates):
        order = []
        blank = []
        allPermanent = True
        for i, pair in enumerate(coordinates):
            sq = self.getSquare(pair)
            if sq.isPermanent():
                order.append(i)
            else:
                blank.append(i)
                allPermanent = False
        return tuple(order + blank), allPermanent
 

    def _findIntersectingClue(self, pair, directionOfClue):
        prev = pair
        while self.isFillableSquare(pair):
            prev = pair
            pair = Board_helper.updatePairBackward(pair, directionOfClue)
        return prev


    def numberItIfItsUnnumbered(self, pair, counter):
        if not self.getSquare(pair).isClueSquare():
            self.getSquare(pair).setNumber(counter)
            counter += 1
        return counter


    def isUnnumbered(self, pair):
        return not self.getSquare(pair).isClueSquare()


    def findClueSpots(self):
        clues = []
        counter = 1
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.isBlackSquare((i, j)):
                    pass
                else:
                    # again use order very intentionally to not error out. 
                    if i == 0 or self.isBlackSquare((i - 1, j)):
                        clues.append(("down", i, j))
                        counter = self.numberItIfItsUnnumbered((i, j), counter)
                    if j == 0 or self.isBlackSquare((i, j - 1)):
                        clues.append(("across", i, j))
                        counter = self.numberItIfItsUnnumbered((i, j), counter)
        return clues


    def coordWord(self, pair, direction):
        length = 0
        locationsInvolved = []
        while self.isFillableSquare(pair):
            locationsInvolved.append(pair)
            pair = Board_helper.updatePairForward(pair, direction)
            length += 1
        return locationsInvolved, length


    def isOnBoard(self, pair):
        return pair[0] < self.height and pair[0] >= 0 and pair[1] < self.width and pair[1] >= 0


    def assignWord(self, startLoc, direction, word, permanent = False):
        pair = startLoc
        for i, letter in enumerate(word):
            if direction == "across":
                pair = (startLoc[0], startLoc[1]  + i)
            elif direction == "down":
                pair = (startLoc[0] + i, startLoc[1])
            self.assignCharacter(pair, letter, permanent)


    def isBlackSquare(self, pair):
        return self.getSquare(pair).isBlack()


    def isFillableSquare(self, pair):

        # uses order of conditions very intentionally. :)
        return self.isOnBoard(pair) and not self.isBlackSquare(pair)

    def getSquare(self, pair):
        if self.isOnBoard(pair):
            return self.board[pair[0]][pair[1]]
        raise ValueError("not on board")

    def getValue(self, pair):
        return self.getSquare(pair).getValue()

    def setBlack(self, pair):
        self.getSquare(pair).makeBlack()

    def assignCharacter(self, pair, seq, permanence=False):
        self.getSquare(pair).setValue(seq, permanence)

    def disp_board(self):

        display  = ""
        # display = "_" * 24 + "\n" 
        for i in self.board:
            #display += "|"
            for j in range(len(i)):
                if i[j].isBlack():
                    val = " " + ".".center(5) + "\t"
                else:
                    val = i[j].getValue()
                    if i[j].isClueSquare():
                        val = " " + val.center(5) + "\t"
                        pass
                        #val = str((i[j]).getNumber()).translate(translation) + val.center(5) + "\t"
                    else:
                        val = " " + val.center(5) + "\t"
                display += val +  "|"
            display += "\n"
            #display += "\n" + "_" * 24 +"\n"
        #display += "_" * 24
        return display
        print (display)

    def compress_board(self):
        string = ""
        for i in self.board:
            for j in range(len(i)):
                if i[j].isBlack():
                    string += "$"
                else:
                    string += i[j].getValue()
        return string




    # def createGUI(self, success):
    #     
    #     root = tkinter.Tk(  )
    #     for row, i in enumerate(self.board):
    #        for j in range(len(i)):
    #             if i[j].isBlack():
    #                 val = " ."
    #                 tkinter.Label(root, text= val + "\t", borderwidth=1, bg="black").grid(row=row,column=j)
    #             else:
    #                 val = i[j].getValue()
    #                 if i[j].isClueSquare():
    #                     val = str((i[j]).getNumber()).translate(translation) + val 
    #                 else:
    #                     val = " " + val
    #                 color = random.choice(["blue","red", "white", "yellow"] )
    #                 tkinter.Label(root, text= val + "\t").grid(row=row,column=j)
    #     for j, setOfClues in enumerate(self.dispClues(success)):
    #         tkinter.Label(root, text = setOfClues).grid(row = len(self.board), column = j, sticky = "W")
    #     root.mainloop(  )
    #     return root
    def clearWord(self, startLoc, direction, length):
        pair = startLoc
        for i in range(length):
            if direction == "across":
                pair = (startLoc[0], startLoc[1]  + i)
            elif direction == "down":
                pair = (startLoc[0] + i, startLoc[1])
            self.assignCharacter(pair, "")



    # notice, ClueSpots I could find really inefficiently by only analyzing the empty squares and not using the existing
    # board information. This was a n^4 algo.

    def dispClues(self, success):
        string = "ACROSS\n"
        for i in success[0]:
            for element in i:
                string += str(element) + " "
            string = string[:-1]
            string += "\n"
        stringDown = "DOWN\n"
        for j in success[1]:
            for element in j:
                stringDown += str(element) + " "
            stringDown = stringDown[:-1]
            stringDown += "\n"
        return string, stringDown

    def clearBoard(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                square = self.getSquare((i, j))
                if not square.isPermanent():
                    square.setValue("", False)


## _______________________________________________________________________________________________________##

def main():
    b = Board(5, 5, empty_squares=None, compressedBoard="$AWS$LLAMAOPTICTHERE$ARK$")

if __name__ == "__main__": 
    main() 