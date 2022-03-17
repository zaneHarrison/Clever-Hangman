"""
Created on 10/28/2020

@author: zaneh
"""
def funct(filename):
    words = open(filename, 'r')
    randomWordList = words.read().split('\n')
    for word in randomWordList:
        if word[-3:] == 'ole' or word[-3:] == 'oul' or word[-3:] == 'ull' or word[-3:] == 'oll' or word[
                                                                                                   -3:] == \
                'oal' or word[-3:] == 'old':
            print(word)

if __name__ == '__main__':
    print(funct('lowerwords.txt'))
