import os
import random
from time import sleep
import numpy as np
abc = "ABCDEFGHJK"

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

def board_10x10_init():
    return np.array(np.array_split(list([0] * 100),10))

def drew_cage(board, mode = 0):
    cage = [''] * 22
    # abc = "ABCDEFGHJK"
    fpics = ['  ', '██', '░░', '╺╸', '▞▞','XX', '░░']
    if mode == 1:
        fpics[1] = fpics[2] = '  '
    if mode == 2:
        fpics[2] = '  '
    cage[0] = "   1  2  3  4  5  6  7  8  9  10"
    cage[1] = "  ┏" + "━━┳" * 9 + "━━┓"
    for i in range(10):
        cage[2 + i * 2] = abc[i] + ' ' + '┃'
        for j in range(10):
            cage[2 + i * 2]+= fpics[board[i, j]] + "┃"
        cage[3 + i * 2] = '  ┣' + "━━╋" * 9 + "━━┫"
    cage[21] = "  ┗" + "━━┻" * 9 + "━━┛"
    for el in cage:
        print(el)

def arr_coor(s):
    k = ''
    for el in s:
        k+= el.center(1 + 2 * el.isalpha())
    k = k[1:].split(' ')
    if len(k) == 4:
        if k[0] > k[2]:   [k[0],k[2]] = [k[2],k[0]]
        if k[1].isdigit() and k[3].isdigit() and int(k[1]) > int(k[3]):   [k[1], k[3]] = [k[3], k[1]]
    if len(k) == 2: k*= 2
    return k

def is_ship_valid(s, board, ships, human = True):
    # abc = "ABCDEFGHJK"
    if not s: return False
    k = arr_coor(s)
    if (len(k) != 2 and len(k) != 4) or \
            k[0] not in abc or k[2] not in abc or\
            not k[1].isdigit() or not k[3].isdigit() or\
            int(k[1]) not in range(1,11) or int(k[3]) not in range(1,11):
        print('Wrong input')
        return False
    if k[0] != k[2] and k[1] != k[3]:
        print('Ship should be only in vertical or horizontal position')
        return False
    size = max(abc.index(k[2]) - abc.index(k[0]), int(k[3]) - int(k[1])) + 1
    if size > 4:
        print("Ship can't be longer than 4")
        return False
    if ships[4 - size] == 0:
        print('Not more available this size of ships')
        return False
    for i in range(2):
        k[i*2] = abc.index(k[i*2])
        k[i*2 + 1] = int(k[i*2 + 1]) - 1
    check_zone = sum(sum(board[k[0]:k[2] + 1, k[1]:k[3] + 1]))
    if check_zone:
        if human:
            print("Ship couldn't be set in this location")
        return False
    return True

def set_ship(s, board, ships):
    # abc = "ABCDEFGHJK"
    k = arr_coor(s)
    for i in range(2):
        k[i*2] = abc.index(k[i*2])
        k[i*2 + 1] = int(k[i*2 + 1]) - 1
    board[max(k[0]-1,0):min(k[2] + 2,10), max(k[1]-1,0):min(k[3] + 2,10)] = 2
    board[k[0]:k[2]+1,k[1]:k[3]+1] = 1
    size = max(k[2]-k[0], k[3]-k[1])
    ships[3 - size]-= 1
    return [board, ships]

def input_ships():
    example = True
    board = board_10x10_init()
    ships = list(range(1,5))
    while sum(ships):
        cls()
        drew_cage(board)
        print('You have:')
        for i in range(4):
            if(ships[i]):
                print(f'Size {4-i}: ' + '██' * (4 - i) + f' x {ships[i]}' * (ships[i] > 1))
        print('Set your ships')
        if example:
            print('For example enter "D3F3" or C8')
        example = False
        s = False
        while not is_ship_valid(s, board, ships):
            s = input().upper()
        [board, ships] = set_ship(s, board, ships)
    print(ships)
    return board

def comp_ships():
    board = board_10x10_init()
    # abc = "ABCDEFGHJK"
    ships = [4,3,3,2,2,2,1,1,1,1]
    for size in ships:
        s = False
        while not is_ship_valid(s, board, [1,1,1,1], False):
            if bool(random.getrandbits(1)):
                a = random.randint(0,9)
                b = random.randint(1,11 - size)
                s = abc[a] + str(b) + abc[a] + str(b+size-1)
            else:
                a = random.randint(0,9 - size)
                b = random.randint(1,10)
                s = abc[a] + str(b) + abc[a+size-1] + str(b)
        board,_ = set_ship(s, board, [1,1,1,1])
    return board

def filltype_input():
    t = ''
    while t not in ['A', 'M']:
        t = input("Autofill or Manual? ('A' or 'M') ").upper()
    cls()
    return t == 'A'

def is_target_valid(target, board):
    y = target[0]
    x = target[1:]
    if y not in abc or not x.isdigit():
        print('Wrong coordinates')
        return False
    y = abc.index(y);  x = int(x) -1
    if x not in range(10):
        print('Wrong coordinates')
        return False
    if board[y,x] in [3,4,5,6]:
        print('You already marked this coordinate')
        return False
    return True

def input_target(board, example):
    target_valid = False
    while not target_valid:
        target = input(f'Enter your target{example} ').upper()
        target_valid = is_target_valid(target, board)
    return target

def show_ship(x1, y1, x2, y2, board ):
    x1_ = max(x1-1,0);    x2_ = min(x2+1,9)
    y1_ = max(y1-1,0);    y2_ = min(y2+1,9)
    for i in range(x1_,x2_+1):
        for j in range(y1_, y2_ + 1):
            if board[j,i] == 5:
                board[j,i] = 4
            elif board[j,i] == 2:
                board[j,i] = 6
    return board

def burn(x,y, board):
    if (x == 0 or board[y, x - 1] not in [1,5]) and \
        (x == 9 or board[y, x + 1] not in [1,5]) and \
        (y == 0 or board[y - 1, x] not in [1, 5]) and \
        (y == 9 or board[y + 1, x] not in [1, 5]):
            board = show_ship(x,y,x,y,board)
    else:
        if (x and board[y,x-1] == 5) or (x < 9 and board[y,x+1] == 5):
            x1 = x; x2 = x
            while x1 > 0 and board[y,x1] == 5:  x1-= 1
            while x2 < 9 and board[y,x2] == 5:  x2+= 1
            if 1 not in [board[y,x1],board[y,x2]]:
                board = show_ship(x1+1,y,x2-1,y, board)
        elif (y and board[y-1,x] == 5) or (y < 9 and board[y+1,x] == 5):
            y1 = y; y2 = y
            while y1 > 0 and board[y1,x] == 5:  y1-= 1
            while y2 < 9 and board[y2,x] == 5:  y2+= 1
            if 1 not in [board[y1,x],board[y2,x]]:
                board = show_ship(x,y1+1,x,y2-1, board)
    return board

def fire(board, target):
    y = abc.index(target[0])
    x = int(target[1:]) - 1
    lucky = (board[y,x] == 1)
    if board[y,x] in [0,2]:
        board[y,x] = 3
    if board[y,x] == 1:
            board[y,x] = 5
            if x and y:   board[y-1,x-1] = 6
            if x and y < 9: board[y+1,x-1] = 6
            if x < 9 and y < 9: board[y+1,x+1] = 6
            if x < 9 and y: board[y-1,x+1] = 6
            board = burn(x,y, board)

    return [board, lucky]

def space_avaiable(board):
    s = 0
    for i in range(10):
        for j in range(10):
            if board[j,i] in [0, 1, 2]:
                s+= 1
    return s

def take_coord(n, board):
    s = 0
    for i in range(10):
        for j in range(10):
            if board[j,i] in [0, 1, 2]:
                if s == n:  return [i,j]
                s+= 1

def comp_target(board):
    n = random.randint(0,space_avaiable(board) - 1)
    [x,y] = take_coord(n, board)
    target = abc[y] + str(x+1)
    return target

def win_check(board):
    s = 0
    for i in range(10):
        for j in range(10):
            s+= (board[j,i] == 4)
    return s == 20

# Start the Game!

print('Battleship'.center(35))

boards = np.array([board_10x10_init() for i in range(2)])
lucky = False
player1 = True
example = ' (for example "D5")'

if filltype_input():
    boards[0] = comp_ships()
else:
    boards[0] = input_ships()
boards[1] = comp_ships()

while not win_check(boards[0]) and not win_check(boards[1]):
    cls()
    drew_cage(boards[0], 2)
    drew_cage(boards[1], 1)
    if player1:
        print('Your turn')
        target = input_target(boards[1], example)
        example = ''
        [boards[1],lucky] = fire(boards[1], target)
        if not lucky:   player1 = False
    else:
        print('Computer turn')
        sleep(1)
        target = comp_target(boards[0])
        print(target)
        sleep(2)
        [boards[0], lucky] = fire(boards[0], target)
        if not lucky:   player1 = True

cls()
drew_cage(boards[0], 2)
drew_cage(boards[1], 2)

if win_check(boards[1]):
    print('You won!')
else:
    print('You lose!')
