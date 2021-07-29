from studyw import StudyW
from studyw import puzzling_word
from studyw import cheering
from time import sleep
import os

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

def quote_split(quote):
    split_index = quote[::-1].index('"')
    split_index = len(quote) - split_index * (split_index > -1)
    return [quote[1:split_index-1], quote[split_index+1:]]

def hardest(text):
    all_words = [word.strip(';:,.\'[]<>?') for word in text.split(' ')]  # clean list all words
    # all_words = sorted(all_words, key = len, reverse = True)  # sorted by length
    hard_words = list(filter(lambda word: len(word) > 3, all_words))
    return hard_words

def longest(text):
    body, ref = quote_split(text)
    return max([len(el) for el in body.split(' ')])  # + [len(ref)])

def puzzling(text, hiden):
    body, ref = quote_split(text)
    body = " ".join([puzzling_word(word, hiden, '_') for word in body.split(' ')])
    # ref = puzzling_word(ref, hiden, '_')
    sub_result = f'"{body}" {ref}'
    result = ''
    for i in range(len(text)):
        if not text[i].isalpha() or sub_result[i] != '_':
            result+= text[i]
        else:
            result+= '_'
    return result

def quotes_compare(q1, q2):
    correct = True
    q = ''
    q1 = q1.lower()
    q2 = q2.lower().ljust(len(q1))
    for i in range(len(q1)):
        q += f'\x1b[{91+ (q1[i] == q2[i])}m{q1[i]}\x1b[0m'
    print(q)
    return '\x1b[91' not in q

class StudyQ:
    def __init__(self, quote, tip):
        self.quote = quote
        self.body, self.ref = quote_split(quote)
        self.tip = tip
        self.progress = 0
        self.hard_words = hardest(self.body)
        self.study_words = False
        self.words = [StudyW(word) for word in self.hard_words]
        self.size = longest(quote)
        self.hiden = 1
        self.timer = 10
        self. progress = 0
        self.puzzled = puzzling(quote, self.hiden)
        self.menu = ''
    def choose_study_mode(self):
        n = len(self.hard_words)
        print(f"You have {n} letter{'s' * (n > 1)} with more than three letters:")
        print(", ".join([word for word in self.hard_words]))
        answer = input('Do you want memorize words first? (Y/N) ').lower()
        if answer == 'xxx':
            return 1
        self.study_words = len(answer) and answer[0] == 'y'
        return 3
    def get_quote(self):
        cls()
        print(f'{self.menu}\n\n{self.puzzled}\n\nEnter the quote (only the part inside of "....")')
        entered = input()
        if entered == 'xxx':    return 'xxx'
        if quotes_compare(self.body, entered):
            self.progress = int(100 * self.hiden / self.size)
            cheering()
            print(f"Progress: {self.progress}%")
            self.hiden += 1
            self.puzzled = puzzling(self.quote, self.hiden)
        else:
            print("Let's try again")
        print()
    def memorize(self):
        print('Tip:', self.tip)
        print(self.quote)
        print('Memorize ...')
        return input('Enter to continue ')
    def learning(self):
        while self.hiden <= self.size:
            if self.memorize() == 'xxx':    return
            if self.get_quote() == 'xxx':   return
        self.progress = 0
        self.puzzled = puzzling(self.quote, 1)
        self.hiden = 1
    def go(self, menu):
        self.menu = menu
        if self.study_words:
            for word in self.words:
                x = word.learning(menu)
                if x == 'xxx':  return 2
            return 3
        else:
            self.learning()
            return 2


