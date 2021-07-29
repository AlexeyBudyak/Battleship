from random import shuffle
from random import randint
from studyq import StudyQ
from studyq import quote_split

class Quote:
    def __init__(self, quote, tip):
        self.quote = quote
        self.body, self.ref = quote_split(quote)    # from studyq.py
        self.tip = tip
        self.study = StudyQ(quote, tip)
    def __str__(self):
        return self.quote

class Quotes:
    def __init__(self, text):
        self.text = text
        self.arr_data = list(text.split('\n'))
        self.all = [Quote(quote,tip) for quote, tip in zip(self.arr_data[::2], self.arr_data[1::2])]
        self.picked_num = None
        self.picked = None
        self.study = None
    def __str__ (self):
        return "\n".join([f"{i}. {s}" for i,s in enumerate(self.arr_data[::2], 1)])
    def shuffle(self):
        shuffle(self.all)
    def pick_quote(self):
        n = input(f"Enter a quote # to study (1 - {len(self.all)}) or anything for a random pick ").lower()
        if n == 'xxx':
            return 0
        if n.isdigit() and int(n) in range(1, len(self.all) + 1):
            self.picked_num = int(n)
        else:
            self.picked_num = randint(1, len(self.all))
        self.picked = self.all[self.picked_num-1]
        return 2
