def oppositeDirection(direction):
        if direction == "across":
            return "down"
        elif direction == "down":
            return "across"

def noneFound(num):
    if num:
        return False
    return True

def addWordToAllRelevantTries(word, tries):
    for length, order in tries:
        if length == len(word):
            alteredWord = putWordIntoCustomizedOrder(word, order)
            tries[(length, order)] = tries[(length, order)].addWord(alteredWord)
    return tries

def removeWordFromAllRelevantTries(word, tries):
    for length, order in tries:
        if length == len(word):
            #print(tries[(length, order)].getSize())
            alteredWord = putWordIntoCustomizedOrder(word, order)
            tries[(length, order)] = tries[(length, order)].dropWord(alteredWord)
            #print(tries[(length, order)].getSize())
    return tries

def alternate(list1, list2):
    num = min(len(list1), len(list2))
    result = [None]*(num*2)
    result[::2] = list1[:num]
    result[1::2] = list2[:num]
    result.extend(list1[num:])
    result.extend(list2[num:])
    return result

def putWordIntoCustomizedOrder(word, order):
    string = ""
    for i in order:
        string += word[i]
    return string

def determineAlteredPrefix(word, order):
    string = ""
    for i in order:
        character = word[i]
        if character == "0":
            break
        else:
            string += character
    return string

def putListIntoCustomizedOrder(oldlist, order):
    listy = [[] for i in range(len(oldlist))]
    for a, i in enumerate(order):
        listy[a] += oldlist[i]
    return listy


def putCustomizedOrderWordIntoEnglish(scramble, order):
    word = ["0" for i in range(len(scramble))]
    for a, i in enumerate(scramble):
        correctLocation = order[a]
        word[correctLocation] = i
    return "".join(word)

def howManyComboInListOfLists(listy):
    number = 1
    for i in listy:
        number *= len(i)
    return number

def innerLoopsANDouterSimulations(number, a, b):
    if number < 10000:
        return number, number
    return int(number / a), int(number / b)

def findRow(spot, w):
    return int(spot / w)
def findCol(spot, w):
    return spot % w


def updatePairForward(pair, direction):
    if direction == "across":
        return (pair[0], pair[1] + 1)
    elif direction == "down":
        return (pair[0] + 1, pair[1])


def updatePairBackward(pair, direction):
        if direction == "across":
            return (pair[0] - 1, pair[1])
        elif direction == "down":
            return (pair[0], pair[1] - 1)