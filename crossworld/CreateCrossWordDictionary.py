# Dictionary Set up:

# Start with webster unabbridged.

# add places (cities, states, provinces, countries, parks, oceans, seas, deserts, mountains)
# add common names, celebrities, artists, musicians, 
# TV shows
# movies
# common abbreviations
# common books
# brand names
# companies
# organizations
import time
import os
import sys
import json

def listFromJSONFILE(file):
    with open(file, "r") as read_file:
        words = json.load(read_file)
    return words

def dictFromJSONFILE(file):
    with open(file, "r") as read_file:
        words = json.load(read_file)
    d = {}
    for word in words:
        if "-" in word:
            continue
        elif " " in word:
            continue
        elif len(word) > 2:
            d[word] = 1
    return d

def dictFromTXTFILE(file):
    words = {}
    with open(file, "r") as read_file:
        for line in read_file:
           key = line.split()

           if key[0].isalpha():

                words[key[0].upper()] = 1

    return words

def Merge(dict1, dict2): 
    dict1.update(dict2)


def mergeFolderOfDicts(startD, folder):
    mergedDicts = startD
    for file in os.listdir(folder):
        newD = dictFromTXTFILE(folder + file)
        mergedDicts = Merge(empty, newD)
    return mergedDicts

def dictionaryToJSON(d, file):
    with open(file, 'w') as outfile:  
        json.dump(d, outfile)

def lengthOfLongestWord(d):
    maxLength = 0
    for i in d:
        if len(i) > maxLength:
            maxLength = len(i)
    return maxLength


def listOfDWordSize(d):
    maxLength = lengthOfLongestWord(d)
    listOfDictionariesByWordSize = [{} for i in range(maxLength)]
    #print(len(listOfDictionariesByWordSize))
    for i in d:
        listOfDictionariesByWordSize[len(i) - 1][i] = 1
    listOfDictionariesByWordSize = listOfDictionariesByWordSize[2:]
    return listOfDictionariesByWordSize


def listOfDictionariesIgnoringWordsShorterThan(wordLength, maxWordLength, words):
    listOfDictionariesByWordSize = [{} for i in range(maxWordLength)]
    for i in words:
        listOfDictionariesByWordSize[len(i) - 1][i] = 1
    listOfDictionariesByWordSize = listOfDictionariesByWordSize[wordLength - 1:]
    return listOfDictionariesByWordSize

