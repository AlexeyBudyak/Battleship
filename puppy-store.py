from random import *
from time import sleep
import os

def cls():
    os.system(['cls', 'clear'][os.name == 'posix'])

def show_building(lvl, arr):
    corner = '      ┏'
    for i in range(lvl):
        wall = '      ┃ '
        if i == 1: corner = '      ┣'
        if i == lvl - 2:    wall = '┏━━━━┓┃ '
        if i == lvl - 1:
            corner = '┃Dogs┃┣'
            wall = '┗┳━━┳┛┃ '
        if len(arr) >= lvl - i:
            wall += f"🍖 {arr[lvl-1-i]['food']}% 🐕 {'💩 ' * arr[lvl-1-i]['poop']}{arr[lvl-1-i]['name']}"
        print(corner + '━' * 20)
        print(wall)
    print('━┻━━┻━┻' + '━' * 25)


def show_gold(gold, customers):
    print('💰', f"${gold}", '|', "  ".join(customers))
    print('━' * 32)

def random_dog(dogs, food = 100):
    male_names = ['Mango', 'Rex', 'Cipher', 'Dunkin', 'Pete', 'Rocky', 'Jack', 'Milo', 'Chewy', 'Jasper',
                  'Zeus', 'Boomer', 'Charlie', 'Gunner', 'Rooney', 'Winston', 'Odin', 'King', 'Nickel',
                  'Disel', 'Gus', 'Baron', 'Fritz', 'Alex']
    female_names = ['Bayley', 'Bella', 'Verona', 'Bony', 'Chance', 'Koda', 'Sierra', 'Shusha', 'Agata',
                    'Shelby', 'Chelsie', 'Lana', 'Nala', 'Luna', 'Lexi', 'Maggi', 'Siena', 'Penny', 'Delta',
                    'Belen', 'Anna']
    dog = {
        'name': 'Noname',
        'gender': ['M', 'F'][randint(0, 1)],
        'food': food,
        'poop': 0
    }
    if dog['gender'] == 'M':
        names = male_names
    else:
        names = female_names
    for el in dogs:
        if el['name'] in names:
            names.remove(el['name'])
    dog['name'] = choice(names)
    return dog

def show_customer(customer, dogs):
    buy_options1 = ['Hello, I would like to buy ', 'Gimme ', 'I want to buy ', 'May I have ']
    buy_options2 = ['I can offer ', 'The best I can give ', 'How about ', 'Me pay you ']
    sell_option1 = ['I want give away ', 'I don\'t need anymore ', 'Could you take ', 'Wish you take ']
    excuses = ['I have allergy on fur', 'We moved to other place', 'This dog too old', 'Vet bills are too expensive',
               'I all the time on my job', 'I need personal life', 'No comment, just take it', 'I bought another dog']
    excuses_m = ['He chew my shoes', 'He pees on my furniture', 'He bite my mom', 'He pooped on my bed',
                 'He barks a lot', 'He ate my hat', 'My son have allergy on him', 'He is lazy', 'He is too active',
                 'He is very agressive', 'My family don\'t like him', 'He became blind',
                 'I can\'t care about him anymore', 'I can\'t afford him', 'Don\'t have enout time for him',
                 'He doesn\'t like my cat', 'I\'m tired of him']
    excuses_f = ['She chew my laptop', 'She pees on carpet', 'She bite my friend', 'She pooped in me boots',
                 'She barks often', 'She ate too much', 'Can\'t control her', 'She is lazy', 'She is too active',
                 'She is agressive', 'She didn\'t bark on thefts', 'She became ugly', 'I can\'t afford her',
                 'She doesn\'t like my cat']
    rehoming = ['Keep it for free', 'No rehoming fee', 'I don\'t accept money for my friend',
                'Make sure you can find a good home for my dog', 'I don\'t worry about payment', 'Please, take it!']
    selling = ['I invested a lot, I need', 'You must pay me', 'I want', 'I\'m asking', 'Rehoming fee is']
    prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200]

    if len(dogs) and getrandbits(1):
        dog = choice(dogs)
        print(customer + ' ' + choice(buy_options1) + dog['name'])
        offer_price = choice(prices)
        print('    ' + choice(buy_options2) + '$' + str(offer_price))
        return [dog, offer_price, True]

    dog = random_dog(dogs, 110)
    excuses+= [excuses_f, excuses_m][dog['gender'] == 'M']

    rate = (randint(1, 100) < 10) * choice(prices)
    print(customer + ' ' + choice(sell_option1) + dog['name'])
    print("    " + choice(excuses))
    if rate:
        print(f"{choice(selling)} ${rate}")
    else:
        print(choice(rehoming))
    return [dog, rate, False]

def del_dog(dogs, name):
    dog_index = next(i for i in range(len(dogs)) if dogs[i]['name'] == name)
    dogs.pop(dog_index)
    return dogs

def ac(n):   # add customer
    return choices(['👩', '🧑', '🕵️',  '👮‍', '👵', '🧒', '👦', '👧', '🧓', '👴', '🧔'],  k=n)

def upgrade_lvl(lvl, gold):
    cost = (lvl - 1) * 500
    print(f"Upgrade for the next level will cost ${cost}")
    if cost > gold:
        print("You don't have enough money for upgrade")
        return lvl, gold
    confirm = input("Do you want to upgrade the store? (Y/N) ").lower()
    if confirm == 'y':
        return lvl + 1, gold - cost
    return lvl, gold

def show_cemetry(dogs, cemetry, reason, del_dogs = True):
    if len(cemetry) == 1:
        print(f'A dog died from {reason}:')
    else:
        print(f'Dogs died from {reason}:')
    for name in cemetry:
        print(f"🐕 {name}")
        if del_dogs:
            dogs = del_dog(dogs, name)
    return dogs

def dog_validator(question):
    no_feed = " you can't feed dog at this time"
    print(question, '(Enter dog\'s name or number):')
    for i, el in enumerate(dogs):
        print(f"{i+1} {el['name']}")
    dog = input().lower()
    if dog.isdigit():
        if int(dog) - 1 not in range(len(dogs)):
            print("We don't have a dog with this number," + no_feed)
            return -1
        else:
            return int(dog) - 1
    for i, el in enumerate(dogs):
        if el['name'].lower() == dog:
            return i
    print("We can't find a dog with this name," + no_feed)
    return -1

def input_feeding(dogs, gold):
    print('Feeding cost: 1% - $1')
    if gold == 0:
        print('You have no money to feed a dog')
        return [dogs, gold]
    index = dog_validator("Which dog you want feeding?")
    if index == -1:
        return dogs, gold
    print(f"You fed {dogs[index]['name']}")
    new_food = min(110 - dogs[index]['food'], gold)
    dogs[index]['food'] += new_food
    return dogs, gold - new_food

def input_cleaning(dogs):
    index = dog_validator("From which dog you want pick up poop?")
    if index == -1:
        return dogs
    print(f"You cleaned after {dogs[index]['name']}")
    dogs[index]['poop'] = 0
    return dogs

lvl = 2
gold = 0
customers = ac(5)
dogs = [random_dog([]), random_dog([])]
cemetry = []
enter = ''
deal = ''
offer = {}
while enter != 'x':
    cls()
    print('🐕 Puppy Store 🐕'.center(30))
    show_building(lvl, dogs)
    the_customer = customers.pop(0)
    customers+= ac(1)
    show_gold(gold, customers)
    offer = show_customer(the_customer, dogs)
    print()
    print('Enter your action:')
    print('A - Accept,  D - Decline, F - Feed, C - Clean, U - upgrade, X - Exit')
    enter = input().lower()
    if enter == 'u':
        [lvl, gold] = upgrade_lvl(lvl, gold)
    if enter == 'd':
        print('You declined offer')
    if enter == 'a':
        if offer[2]:
            dogs = del_dog(dogs, offer[0]['name'])
            gold += offer[1]
            print('You sold the dog')
        elif lvl == len(dogs):
            print('Not available space in the dog store, you can\'t accept anymore dogs for now')
        elif gold < offer[1]:
            print('You don\'t have enough money to buy this dog')
        else:
            dogs.append(offer[0])
            gold-= offer[1]
            print('You took the dog')
    if enter == 'f':
        dogs, gold = input_feeding(dogs, gold)
    if enter == 'c':
        dogs = input_cleaning(dogs)

    sub_cemetry = []
    for i in range(len(dogs)):
        dogs[i]['food'] = dogs[i]['food'] - 10
        if dogs[i]['food'] <= 0:
            sub_cemetry.append(dogs[i]['name'])
    if len(sub_cemetry):
        dogs = show_cemetry(dogs, sub_cemetry, 'hunger')
        cemetry+= sub_cemetry
    sub_cemetry = []
    for i in range(len(dogs)):
        dogs[i]['poop']+= choice([0,0,1])
        if dogs[i]['poop'] > 3:
            sub_cemetry.append(dogs[i]['name'])
    if len(sub_cemetry):
        dogs = show_cemetry(dogs, sub_cemetry, 'infesting')
        cemetry+= sub_cemetry

    if enter != 'x':
        print("Waiting for a new customer...")
        sleep(2)

print('The END\n')
if len(cemetry):
    show_cemetry(dogs, cemetry, 'hunger or infesting', del_dogs = False)
