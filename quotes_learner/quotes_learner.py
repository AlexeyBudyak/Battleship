from file import File
from quotes import Quotes
from intro import intro
from menu import Menu
import os

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

intro()
input('Enter to continue')
menu = Menu()
f = File()

while menu.lvl == 0:
    cls()
    f.pick_file()
    try:
        menu.lvl1(f.name)
        data = Quotes(f.load())
    except:
        menu.lvl = -1
    # data.shuffle()
    while menu.lvl == 1:
        cls()
        print(menu)
        print(f'\n{data}\n')
        menu.new_lvl(data.pick_quote())
        while menu.lvl == 2:
            menu.lvl2(data.picked_num)
            cls()
            print(menu)
            print(f'\n{data.picked}\n')
            menu.new_lvl(data.picked.study.choose_study_mode())
            while menu.lvl == 3:
                cls()
                print(f"{menu}\n")
                menu.new_lvl(data.picked.study.go(str(menu)))

print('\nWill glad to see you again!')
