import Board
import Board_helper
import Square
import Trie
import time
import CreateCrossWordDictionary
import datetime

def createOnePuzzle(h, w, dictionaries, emptys=[(0, 0), (4, 4)]):
    puzzles = []
    countSucc = 0
    game = Board.Board(h, w, emptys)
    across = [(direction, row, col) for direction, row, col in game.clueDirAndStart if direction == "across"]
    down = [(direction, row, col) for direction, row, col in game.clueDirAndStart if direction == "down" ]
    triesAltered = game.generateTriesByNeed(dictionaries, across, down)
    bestResult = 99999
    bestPair = (None, None)
    success = [False, False, False]
    while not success[0]:
        game.clearBoard()
        success = game.fillInPuzzle(triesAltered, across, down, 5, 3)
        if success[0]:
            return game, success
        for word in success[2]:
            triesAltered = Board_helper.addWordToAllRelevantTries(word, triesAltered)
            #print(word)

def main():
    h = 5
    w = 5
    maxLength = max(h, w)
    storage = {}
    storage["numRows"] = h
    storage["numCols"] = w



    dictJSONFILE = "CrossWordDictionaryBest.json"
    d = CreateCrossWordDictionary.dictFromJSONFILE(dictJSONFILE)
    best = CreateCrossWordDictionary.listOfDWordSize(d) # TODO save this as a dictionary.
    while True:
        solution, (across, down, allwords) = createOnePuzzle(h, w, best)
        print(solution.disp_board())
        print("Enter if this is a goodboard, any other key to create a new one")
        response = input()
        if response == "":
            storage["solution"] = solution.compress_board()
            for i, (number, word) in enumerate(across):
                print(solution.disp_board())
                print(number, word)
                print("Please write a clue for this word.")
                clue = input()
                acceptable = False
                while not acceptable:
                    print("Good with this clue?, Enter for yes, anything else for no")
                    notValid = input()
                    if notValid:
                        print("Please write a clue for this word.")
                        clue = input() 
                    else:
                        acceptable = True
                across[i][1] = clue
            storage["across"] = across
            for i, (number, word) in enumerate(down):
                print(number, word)
                print("Please write a clue for this word.")
                clue = input()
                acceptable = False
                while not acceptable:
                    print("Good with this clue?, Enter for yes, anything else for no")
                    notValid = input()
                    if notValid:
                        print("Please write a clue for this word.")
                        clue = input() 
                    else:
                        acceptable = True
                down[i][1] = clue
            storage["down"] = down
            difficulty = "M"
            date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            filename = str(h) + "x" + str(w) + "_no_theme_" + difficulty + "_" + date +".json"
            CreateCrossWordDictionary.dictionaryToJSON(storage, filename)



        else:
            continue


        print(down)
    


if __name__ == "__main__": 
    main() 