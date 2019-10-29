import Queue as queue
import random
import time

# TODO, optimize storage, using none type, using numpy arrays instead of python native arrays. 
# Also update trie to be exactly the tries we need. 

class Trie:
    def __init__(self, value):
        self.value = value
        self.word_finished = False
        self.frequency = 0
        self.children = [None for i in range(26)]

    def getSize(self):
        return self.frequency

    def isSatisfiable(self, constraints):
        pass

    def isTherePossibleWord(self, constraints):
        # PROBLEMATIC - must edit

        currentLetter = self
        word = ""
        for constraint in constraints:
            found = False
            for acceptable_letter in constraint:
                offset = ord(acceptable_letter.upper()) - ord('A')
                nextTrie = currentLetter.children[offset]
                if nextTrie:
                    found = True
                    word += nextTrie.value
                    currentLetter = nextTrie
                    break 
            if not found:
                return False

        if len(word) == len(constraints):
            #print(constraints)
            return True

        return False

    def getChildrenCurrentLetter(self):
        children = []
        for i in self.children:
            if i:
                children.append(i)
        return children

    def randomlyFindNextLetter(self, constraint, currentLetter, word):
        
        candidateLetter = random.choice(constraint).upper()
        inChildren = False
        loops = 0
        while not inChildren:
            #print(candidateLetter)
            if loops > 20:
                return False

            offset = ord(candidateLetter) - ord('A')

            if currentLetter.children[offset]:

                currentLetter = currentLetter.children[offset]
                word += currentLetter.value
                inChildren = True
            else:
                candidateLetter = random.choice(constraint).upper()
            loops += 1
        return currentLetter, word


    def getRandomWordGivenConstraints(self, constraints):
        currentLetter = self
        word = ""
        i = 0
        while not currentLetter.word_finished:
            constraint = constraints[i]
            updatedLetterAndWord = self.randomlyFindNextLetter(constraint, currentLetter, word)
            # if updatedLetterAndWord:
            #     currentLetter, word = updatedLetterAndWord
            # else:
            #     return False
            attempts = 0
            #print(len(constraint))
            while not updatedLetterAndWord and attempts < len(constraint):
                #print(updatedLetterAndWord)
                updatedLetterAndWord = self.randomlyFindNextLetter(constraint,
                 currentLetter, word)
                attempts += 1
            if updatedLetterAndWord:
                currentLetter, word = updatedLetterAndWord
            else:
                return False
            i = i + 1
        return word



    def getRandomWord(self):
        currentLetter = self
        word = ""
        while not currentLetter.word_finished:
            children = currentLetter.getChildrenCurrentLetter()
            i = random.randint(0, len(children) - 1)
            currentLetter = children[i]
            if currentLetter.value:
                word += currentLetter.value
        return word


    def doesWordExist(self, word):
        currentLetter = self
        for i in word:
            i = i.upper()
            nextLetter = currentLetter.isThereChild(i)
            if not nextLetter:
                return False
            currentLetter = nextLetter
        if currentLetter.word_finished:
            return True
        return False

    def frequencyOfPrefix(self, prefix):
        currentLetter = self
        for character in prefix:
            nextLetterExists = currentLetter.isThereChild(character)
            if nextLetterExists:
                currentLetter = nextLetterExists
            else:
                return 0
        return currentLetter.frequency


    def addWord(self, word):
        if not self.doesWordExist(word):
            currentLetter = self
            for character in word:
                character = character.upper()
                nextLetterExists = currentLetter.isThereChild(character)
                if nextLetterExists:
                    currentLetter.frequency += 1
                    currentLetter = nextLetterExists
                    
                else:
                    currentLetter = currentLetter.addChild(character)
                    currentLetter.frequency = 1
            currentLetter.word_finished = True
        return self

    def hasNoChildren(self):
        return not self.getChildrenCurrentLetter()

    def dropWord(self, word, indexOfWord=0):
        self.frequency -= 1
        if indexOfWord == len(word):
            if self.word_finished:
                self.word_finished = False
            if self.hasNoChildren():
                del(self)
                self = None  
            return self
        self.children[ord(word[indexOfWord]) - ord('A')] = self.children[ord(word[indexOfWord])
         - ord('A')].dropWord(word, indexOfWord + 1)
        if self.hasNoChildren() and not self.word_finished:
            del(self)
            self = None
        return self



    def removeChild(self, value):
        offset = ord(value.upper()) - ord('A')
        self.children[offset] = None

    def addChild(self, value):
        offset = ord(value.upper()) - ord('A')
        child = Trie(value)
        self.children[offset] = child
        return child

    def getChildren(self, prefix):

        currentLetter = self
        for character in prefix:
            nextLetterExists = currentLetter.isThereChild(character)
            if nextLetterExists:
                currentLetter = nextLetterExists
            else:
                return False
        childValues = []
        for i in currentLetter.getChildrenCurrentLetter():
            childValues.append(i.value)
        return childValues



    def isThereChild(self, value):
        offset = ord(value.upper()) - ord('A')
        return self.children[offset]


    def printLevels(self):
        q = queue.Queue()
        q.put((self, 0))
        string = ""
        prev = 0
        while not q.empty():
            pair = q.get()
            #print(pair)
            node = pair[0]
            level = pair[1]
            if prev != level:
                string += "\n"
                #print("NEXT LEVEL", level)
            if node:
                for child in node.children:
                    if child:
                        print(child.value, level)
                    q.put((child, level + 1))
                prev = level
        return string

    def printWords(self, word):
        print(self.value)
        children = self.getChildrenCurrentLetter()
        if len(children) == 0:
            print(word + self.value)
        else:
            if self.value:
                word = word + self.value
            if self.word_finished:
                print(word)
            for i in children:
                if i:
                    i.printWords(word)


def triesGroupedByNumberOfLetters(d, maxlen):
    triesNumberOfLetters =  [Trie(None) for i in range(maxlen)]
    for i in d:
        lengthOfWord = len(i)
        if lengthOfWord <= maxlen:
            triesNumberOfLetters[lengthOfWord - 1].addWord(i.upper())
            assert(doesWordExistInListOfTries(triesNumberOfLetters, i.upper(), maxlen))
    return triesNumberOfLetters
def doesWordExistInListOfTries(tries, word, maxLength):
    if len(word) > maxLength:
        raise ValueError("Tries do not store words of length " + str(len(word)))

    return tries[len(word) - 1].doesWordExist(word)


def main():
    t = Trie(None)
    t.addWord("dog")

    t.addWord("abs")
    t.addWord("dig")
    t.addWord("doggy")
    t.addWord("doggo")
    print("HERE WE GO")
    t = t.dropWord("ABS", 0)
    t = t.dropWord("DOG", 0)
    #t.addWord("dog")
    #t = t.dropWord("abs")
    t.printWords("")

    # #print(t.doesWordExist("dog"))
    # #t.printLevels()

    # constraints = [["d"], ["o"], ["g"], ["g"], ["y"]]
    # #word = t.getRandomWordGivenConstraints(constraints)
    # #print(word)

if __name__ == "__main__": 
    main() 


