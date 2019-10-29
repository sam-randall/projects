import Board
import Square
import Trie
import time
import datetime
import CreateCrossWordDictionary
# def triesGroupedByNumberOfLetters(d, maxlen):
#     triesNumberOfLetters = [Trie.Trie(None) for i in range(maxLength)]
#     for i in d:
#         lengthOfWord = len(i)
#         if lengthOfWord <= maxlen:
#             triesNumberOfLetters[lengthOfWord - 1].addWord(i.upper())
#     return triesNumberOfLetters

# def doesWordExistInListOfTries(tries, word, maxLength):
#     if len(word) > maxLength:
#         raise ValueError("Tries do not store words of length " + str(len(word)))
    
    # return tries[len(word) - 1].doesWordExist(word)

# def getCorrectTrie(tries, word):
#     return tries[len(word) - 1]

def assertValid(words, tries, maxL):
    for index, i in words:
        assert(doesWordExistInListOfTries(tries, i, maxL))

def createPuzzlesAutomatically(h, w, numberOfAttempts, dictionaries, emptys):
    puzzles = []
    countSucc = 0
    game = Board.Board(h, w, emptys)

    #game.assignWord((0, 0), "across", "JETER", permanent=True)
    # game.assignWord((1, 0), "across", "ADMAN", permanent=True)
    # game.assignWord((0, 0), "down", "FUCKU", permanent=True)
    #game.assignWord((0, 4), "down", "YEMEN", permanent= True)
    #game.disp_board()
    #game.assignWord((2, 0), "across", "AAHED", permanent = True)
    # ASSIGN THE STUFF HERE
    across = [(direction, row, col) for direction, row, col in game.clueDirAndStart if direction == "across"]
    down = [(direction, row, col) for direction, row, col in game.clueDirAndStart if direction == "down" ]
    triesAltered = game.generateTriesByNeed(dictionaries, across, down)
    bestResult = 99999
    bestPair = (None, None)
    puzzles = {}
    prev = time.time()
    for i in range(numberOfAttempts):
        if i % 1000 == 0:
            print(i)
        game.clearBoard()
        success = game.fillInPuzzle(triesAltered, across, down, 50, 100)
        game.disp_board()
        if success[0]:
            print(time.time() - prev)
            prev = time.time()
            countSucc += 1

            #print(game.disp_board())
            string = game.compress_board()
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            puzzles[string] = date
            print(string)

            #game.createGUI((success[0], success[1]))
        for word in success[2]:
            #print(word)
            triesAltered = Board.addWordToAllRelevantTries(word, triesAltered)

    return puzzles





def main():
    h = 5
    w = 5
    maxLength = max(h, w)
    #allW = CreateCrossWordDictionary.dictFromJSONFILE("CrossWordDictionary.json")
    #listOfDictionaries = CreateCrossWordDictionary.listFromJSONFILE("CrossWordListOfDictionariesBest.json")

    dictJSONFILE = "CrossWordDictionaryBest.json"
    d = CreateCrossWordDictionary.dictFromJSONFILE(dictJSONFILE)
    #print(d["ENNEW"])
    best = CreateCrossWordDictionary.listOfDWordSize(d) # TODO save this as a dictionary. 
    start = time.time()
    countSucc = 0
    #emptys = [(4, 0),(4, 4)]
    #emptys = [(3, 0), (3, 1), (3, 5), (3, 6), (0, 3), (1, 3), (5, 3), (6, 3)]
    numberOfAttempts = 10000
    #print(len(d))
    emptys = [(0, 0), (4, 4)]

    puzzles = createPuzzlesAutomatically(h, w, numberOfAttempts, best, emptys)
    #for sol in puzzles:

    # if answer[0]  != 0:
    #     timePerSuccess = (time.time() - start) / answer[0]
    #     print("TIME PER SUCCESSFUL PUZZLE: ", timePerSuccess)
    # else:
    #     print("No Successes")
    #print("SUCCESS RATE:", countSucc / 100)

if __name__ == "__main__": 
    main() 