from random import shuffle
from time import sleep
import os

size = os.get_terminal_size().columns // 3 or 13

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

def color(s, n):
    # 0 - white, 1 - red, 2 - green, 3 - yellow, 4 - blue
    return f'\x1b[{90 * bool(n) + n}m' + s + '\x1b[0m'

def show_back_cards(n_cards):
    show_cards = ''
    for i in range(3):
        for j in range(min(size, n_cards)):
            if j == size - 1 and size < n_cards:
                show_cards+=['   ','   ','...'][i]
            else:
                show_cards+= ['┏━┓','┃ ┃','┗━┛'][i]
        show_cards+= '\n'
    return show_cards[:-1]

def is_card_fit(card1, card2):
    return card1.rank == card2.rank or card1.clr2 == card2.clr or card2.clr == 0

def show_face_cards(cards, deck_card):
    show_cards = ''
    for line in range(len(cards) // size + bool(len(cards) % size)):
        for i in range(4):
            for j in range(size):
                if line * size + j < len(cards):
                    if i == 3:
                        ref  = f'^{line * size + j+1}'
                        ref = color(ref, is_card_fit(deck_card, cards[line * size + j]) + 1)
                        show_cards += ref + ' ' * (line * size + j < 9)
                    else:
                        show_cards += cards[line * size + j].pic[i]
            show_cards += '\n'
    return show_cards[:-1]

def show_cards(cards, deck_card, open = True):
    return show_face_cards(cards, deck_card) if open else show_back_cards(len(cards))

def card_solid_init(clr, rank):
    return  [color('┏━┓', clr), \
             color(f'┃{rank}┃', clr), \
             color('┗━┛', clr)]

def card_rainbow_init(rank):
    return [color('┏━', 1) + color('┓', 2), \
            color('┃', 4) + str(rank) + color('┃', 2), \
            color('┗', 4) + color('━┛', 3)]

class Card:
    def __init__(self, clr, rank, value):
        self.clr = clr
        self.clr2 = clr
        self.rank = rank
        self.value = value
        self.pic = card_solid_init(clr, rank) if clr else card_rainbow_init(rank)
    def change_color(self, n):
        self.clr2 = n
        self.pic = card_solid_init(n, self.rank) if n else card_rainbow_init(self.rank)



def show_deck(cards):
    s = 'The Deck\n'
    cards = cards[-size + 1:]
    for i in range(3):
        s+= ['┏━┓','┃ ┃','┗━┛'][i]
        for card in cards:
            s+= card.pic[i]
        s+= '\n'
    return s[:-1]

class Deck:
    def __init__(self):
        self.open = True
        self.cards = [Card(c, str(i), i)   for c in range(1,5) for i in range(10)] + \
                     [Card(c, '+', 20) for c in range(1, 5) for i in range(2)] +\
                     [Card(c, 'R', 20) for c in range(1, 5) for i in range(2)] +\
                     [Card(c, 'ø', 20) for c in range(1, 5) for i in range(2)] +\
                     [Card(0, '*', 50) for i in range(4)] + \
                     [Card(0, '+', 50) for i in range(4)]
        shuffle(self.cards)
        i = 0
        while self.cards[i].value > 9:    i+= 1  # To start with a regular card
        self.used = [self.cards.pop(i)]
    def __str__(self):
        return show_deck(self.used)
    def shuffle(self):
        shuffle(self.cards)
    def take(self):
        if len(self.cards):
            return self.cards.pop(0)
        elif len(self.used) > 1:
            self.cards = self.used[:-1]
            shuffle(self.cards)
            self.used = [self.used[-1]]
            return self.cards.pop(0)
        else:
            return Card(0,'x',0)
    def to_used(self, new_card):
        self.used[-1].change_color(self.used[-1].clr)
        self.used+= [new_card]
    def isempty(self):
        return len(self.cards) + len(self.used) == 1

def input_color():
    color_choice = ''
    for i in range(3):
        for j in range(1,5):
            color_choice+= color(['┏━┓',f'┃{j}┃','┗━┛'][i],j)
        color_choice+= '\n'
    print(color_choice[:-1])
    new_color = ''
    while new_color not in ['1', '2', '3', '4']:
        if new_color != '':
            print('Wrong input')
        new_color = input('Choose a new color ')
    return int(new_color)

def best_color(cards):
    colors = [0, 0, 0, 0, 0]
    for card in cards:
        colors[card.clr]+= 1
    colors = colors[1:]
    return colors.index(max(colors)) + 1

class Player:
    def __init__(self, name, deck_card, open = True):
        self.open = open
        self.name = name
        self.cards = []
        self.deck_card = deck_card
        self.fit_cards = []
        self.best_card = 0
        self.total_value = 0
    def __str__(self):
        return f"{self.name} has {len(self.cards)} card{'s' * (len(self.cards) != 1)}\n" + \
                show_cards(self.cards, self.deck_card, self.open)
    def add(self, new_card):
        if new_card.rank != 'x':
            self.cards+= [new_card]
    def check_fit_cards(self, deck_card):
        self.deck_card = deck_card
        self.fit_cards = []
        best_value = -1
        for i,card in enumerate(self.cards):
            if is_card_fit(self.deck_card, card):
                if best_value < card.value:
                    best_value = card.value
                    self.best_card = i
                self.fit_cards.append(i+1)
    def choose_color(self, index):
        self.cards[index].change_color(input_color())
    def auto_choose_color(self, index):
        self.cards[index].change_color(best_color(self.cards))
    def put(self, index):
        return self.cards.pop(index)
    def calculate_value(self):
        self.total_value = sum([card.value for card in self.cards])

def intro_UNO(cards):
    uno_data = [1,0,0,1, 0, 1,0,0,1, 0, 0,1,0,
                1,0,0,1, 0, 1,0,1,1, 0, 1,0,1,
                1,0,0,1, 0, 1,1,0,1, 0, 1,0,1,
                0,1,1,0, 0, 1,0,0,1, 0, 0,1,0,]
    show_cards = ''
    for line in range(4):
        for i in range(3):
            for j in range(13):
                show_cards += ['   ', cards[line * 13 + j].pic[i]][uno_data[line * 13 + j]]
            show_cards += '\n'
    print(show_cards)

def switch_turn(turn, step, num_players, skip):
    return (turn + num_players + step * (skip + 1)) % num_players

def winner(players):
    for i, player in enumerate(players):
        if len(player.cards) == 0:
            return i
    return -1

def input_num_comp():
    num_comp = ''
    while num_comp not in ['1', '2', '3', '4', '5']:
        if num_comp:
            print('Your inpot is not valid')
        num_comp = input('Enter the number of computer opponents (1-5) ')
    return int(num_comp)

def input_choice(fit_cards):
    while True:
        enter = input("Enter card # or T - take, X - exit > ").lower()
        if enter in ['x', 't']:
            return enter
        if enter.isdigit():
            if int(enter) in range(1, len(players[0].cards) + 1):
                if int(enter) in fit_cards:
                    return enter
                else:
                    print("You can't use this card")
            else:
                print('The number out of range')
        else:
            print('Wrong input')

deck = Deck()
intro_UNO(deck.cards)

name = input('What is your name? ')
num_players = input_num_comp() + 1

players = []
for player_index in range(num_players):
    if player_index:
        name = f'Computer #{player_index}'
    players.append(Player(name, deck.used[-1], player_index == 0))
    for i in range(7):
        players[player_index].add(deck.take())
enter = ''
turn = 0
step = 1
skip = False

while winner(players) == -1 and enter != 'x':
    cls()
    players[turn].check_fit_cards(deck.used[-1])
    for j in range(1, num_players):
        print(players[j])
    print(deck)
    players[0].check_fit_cards(deck.used[-1])
    print(players[0])
    skip = False
    while True:
        enter = ''
        if not turn:
            enter = input_choice(players[0].fit_cards)
            if enter == 'x':
                break
            if enter == 't':
                if deck.isempty():
                    turn = switch_turn(turn, step, num_players, skip)
                else:
                    players[0].add(deck.take())
                break
            if enter.isdigit():
                players[0].best_card = int(enter) - 1
        else:
            while len(players[turn].fit_cards) == 0 and not deck.isempty():
                players[turn].add(deck.take())
                players[turn].check_fit_cards(deck.used[-1])
        if len(players[turn].fit_cards) == 0:
            turn = switch_turn(turn, step, num_players, skip)
            break
        act_card = players[turn].cards[players[turn].best_card]

        if act_card.clr == 0:
            if turn:
                players[turn].auto_choose_color(players[turn].best_card)
            else:
                players[0].choose_color(players[turn].best_card)

        deck.to_used(players[turn].put(players[turn].best_card))

        if act_card.rank == 'R':    step *= -1
        if act_card.rank in 'ø':    skip = True

        if turn:
            print(players[turn].name, 'turn ...')
            sleep(2)

        turn = switch_turn(turn, step, num_players, skip)
        if act_card.rank == '+':
            for i in range(2 + (act_card.clr == 0) * 2):
                players[turn].add(deck.take())
            turn = switch_turn(turn, step, num_players, skip)

        break

win_index = winner(players)
if win_index > -1:
    print(f"\n{players[win_index].name} won!\n")
for i in range(num_players):
    players[i].calculate_value()
    print(f"{players[i].name} \t {players[i].total_value * (-1)} points")
