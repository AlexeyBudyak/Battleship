from time import sleep
from random import choice
import os

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

def cheering():
    cheers = ['Good job!', 'You are right', 'You are the best!', 'Awesome!', 'You did it!', 'Right!', 'Correct!',
              'I\'m impressed!', 'You are smart!', 'Perfect!']
    print(choice(cheers))


def show_word(word):
    output = '┏' + '━┳' * (len(word) - 1) + '━┓\n'
    for c in word:
        output+= '┃' + c
    output+= '┃\n'
    output+= '┗' + '━┻' * (len(word) - 1) + '━┛'
    return output

def puzzling_word(word, hiden, mark = '*'):
    if hiden >= len(word):
        return mark * len(word)
    return word[:len(word) - hiden] + mark * hiden

class StudyW:
    def __init__(self, word):
        self.word = word
        self.puzzled = puzzling_word(word, 1)
        # self.puzzled = word[:-1] + '*'
        self.hiden = 1
        self.timer = len(word)
        self. progress = 0
        self.menu = ''
    def __str__(self):
        return show_word(self.puzzled)
    def memorize(self):
        print(show_word(self.word))
        print('Memorize ...')
        return input('Enter to continue ')
    def get_word(self):
        cls()
        print(f"{self.menu}\n\n{self}")
        # print(show_word(self.puzzled))
        enter = input('Enter the word ').lower()
        if enter == 'xxx':  return 'xxx'
        if enter == self.word.lower():
            self.progress = int(100 * self.hiden / len(self.word))
            cheering()
            print(f"Progress: {self.progress}%")
            self.hiden+= 1
            self.puzzled = puzzling_word(self.word, self.hiden)
        else:
            print("Let's try again")
    def learning(self, menu):
        self.menu = menu
        while self.hiden <= len(self.word):
            if self.memorize() == 'xxx':    return 'xxx'
            if self.get_word() == 'xxx':    return 'xxx'
        self.progress = 0
        self.puzzled = self.word[:-1] + '*'
        self.hiden = 1


