"""
@author: Zane Harrison    zlh4
"""

import random

def handleUserInputDebugMode():
    """
    Prompts the user to choose whether to play in debug or play mode. Returns True if they choose debug
    mode, returns False otherwise
    """
    mode = input('Which mode do you want to run: (d)ebug or (p)lay: ')
    if mode == 'd':
        return True
    elif mode == 'p':
        return False


def handleUserInputWordLength():
    """
    Prompts the user for the length of the word to be guessed, returns the user's input as an integer
    """
    wordLength = input('Please enter a value from 5 to 10 to determine the length of the secret word: ')
    return int(wordLength)


def createTemplate(currTemplate, letterGuess, word):
    """
    Takes the current template for the secret word, the current guess, and the secret word and returns the
    updated template for the secret word with '_'s in the places of unguessed letters
    """
    currTemplateMutable = [ch for ch in currTemplate]
    wordMutable = [ch for ch in word]
    for letter in wordMutable:
        if letter == letterGuess:
            index = wordMutable.index(letterGuess)
            currTemplateMutable[index] = letterGuess
            wordMutable[index] = '*'
    new_currTemplate = ''
    for ch in currTemplateMutable:
        new_currTemplate += ch
    return new_currTemplate


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    """
    Takes the current word template, the current guess, a list of words and a boolean value and returns a
    2-tuple containing the new word template and it's corresponding list of matching words
    """
    dict1 = {}
    for word in wordList:
        wordTemplate = createTemplate(currTemplate, letterGuess, word)
        dict1[wordTemplate] = []
    for word in wordList:
        for key in dict1:
            if key == createTemplate(currTemplate, letterGuess, word):
                dict1[key] += [word]
    # print(dict)
    sortedDict = sorted(dict1.items(),
                        key=lambda x: (len(x[1]), x[0].count("_")))  # Second sorting breaks ties
    debugSortedDict = sorted(dict1.items(), reverse=False)
    if debug:
        for (k, v) in debugSortedDict:
            print(k + ' :', len(v))
        print('# keys = ' + str(len(dict1)))
    return sortedDict[-1]


def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    """
    Takes the user's guess, the user's current progress on the word, and the number of misses left; updates
    the number of misses left and indicates whether the user missed
    """
    retList = []
    if guessedLetter not in hangmanWord:
        retList.append(missesLeft - 1)
        retList.append(False)
    elif guessedLetter in hangmanWord:
        retList.append(missesLeft)
        retList.append(True)
    return retList


def handleUserInputDifficulty():
    """
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    """
    print('How many misses do you want? Hard has 8 and '
          'Easy has 12.')
    difficultySetting = input('(h)ard or (e)asy> ')
    if difficultySetting == 'h':
        print('You have 8 misses to guess word \n')
        return 8
    elif difficultySetting == 'e':
        print('You have 12 misses to guess word \n')
        return 12


def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    """
    Creates the string that will be displayed to the user, using the information in the parameters.
    """
    lettersNotGuessedString = 'abcdefghijklmnopqrstuvwxyz'
    for letter in sorted(lettersGuessed):
        lettersNotGuessedString = lettersNotGuessedString.replace(letter, ' ')
    hangmanWordString = ''
    for letter in hangmanWord:
        hangmanWordString += letter + " "
    outputString = 'letters not yet guessed: ' + lettersNotGuessedString + "\nmisses remaining = " + \
                   str(missesLeft) + '\n' + hangmanWordString.strip()
    return outputString


def handleUserInputLetterGuess(lettersGuessed, displayString):
    """
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    """
    print(displayString)
    guess = input('letter> ')
    while guess in lettersGuessed:
        print('you already guessed that')
        guess = input('letter> ')
    return guess


def runGame(filename):
    """
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    """
    debug = handleUserInputDebugMode()
    # print(debug)
    words = open(filename, 'r')
    randomWordList = words.read().split('\n')
    randomLength = int(handleUserInputWordLength())
    randomWordListOfLength = []
    for word in randomWordList:
        if len(word) == randomLength:
            randomWordListOfLength += [word]
    secretWord = random.choice(randomWordListOfLength)
    # print(secretWord)
    missesLeft = handleUserInputDifficulty()
    totalMisses = missesLeft
    hangmanWord = ['_' for letter in secretWord]
    currTemplate = ''.join(hangmanWord)
    lettersGuessed = []

    while True:
        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        if debug:
            displayStringList = (displayString.split('\n'))
            displayStringList = displayStringList[:2] + ["(word is " + secretWord + ')'] + ["# possible "
                                                                                            "words: " +
                                                                                            str(len(
                                                                                                randomWordListOfLength))] \
                                + [
                                    displayStringList[2]]
            debugDisplayString = displayStringList[0] + "\n" + displayStringList[1] + "\n" + \
                                 displayStringList[2] + \
                                 "\n" + displayStringList[3] + "\n" + displayStringList[4]
            displayString = debugDisplayString
        guess = handleUserInputLetterGuess(lettersGuessed, displayString)
        lettersGuessed.append(guess)
        keyValue = getNewWordList(currTemplate, guess, randomWordListOfLength, debug)
        # print(keyValue)
        hangmanWord = [ch for ch in keyValue[0]]
        # print(hangmanWord)
        currTemplate = ''.join(hangmanWord)
        # print(currTemplate)
        randomWordListOfLength = keyValue[1]
        # print(randomWordListOfLength)
        missesLeft = processUserGuessClever(guess, hangmanWord, missesLeft)[0]
        secretWord = random.choice(randomWordListOfLength)
        # if debug:
        # print('word is ' + secretWord)
        if processUserGuessClever(guess, hangmanWord, missesLeft)[1] == False:
            print('you missed: ' + guess + ' not in word')
        if missesLeft == 0:  # If user loses
            print("you're hung!!\nword was " + secretWord)
            print('you made ' + str(len(lettersGuessed)) + ' guesses with ' + str((totalMisses -
                                                                                   missesLeft)) + ' misses\n')
            return False
        if '_' not in hangmanWord:  # If user wins
            print('you guessed the word: ' + secretWord)
            print('you made ' + str(len(lettersGuessed)) + ' guesses with ' + str((totalMisses -
                                                                                   missesLeft)) + ' misses\n')
            return True
        print('\n')


if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    winCount = 0
    lossCount = 0
    play_again = True
    while play_again == True:
        win_loss = runGame('lowerwords.txt')
        if win_loss == True:
            winCount += 1
        elif win_loss == False:
            lossCount += 1
        playAgain = input('Do you want to play again? y or n> ')
        if playAgain == 'y':
            play_again = True
        elif playAgain == 'n':
            play_again = False
    print('You won ' + str(winCount) + ' game(s) and lost ' + str(lossCount))
