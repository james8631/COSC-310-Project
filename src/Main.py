import os.path
from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd

class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password


class Item:
    def __init__(self, name, amount, unit, type):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.type = type


def get_user(first_name, last_name, username, password):
    user = User(first_name, last_name, username, password)
    return user

def get_item(name, amount, unit, type):
    item = Item(name, amount, unit, type)
    return item

def append_user(user):
    with open('user.txt', 'a') as f:
        f.write(user.first_name + ',' + user.last_name + ',' + user.username + ',' + user.password + '\n')

def append_item(item):
    with open('item.txt', 'a') as f:
        f.write(item.name + ',' + str(item.amount) + ',' + item.unit + ',' + item.type + '\n')

def write_user(user_list):
    os.remove('user.txt')  # temp solution, change later
    for i in range(0,len(user_list)):
        append_user(user_list[i])

def write_item(item_list):
    os.remove('item.txt')  # temp solution, change later
    for i in range(0,len(item_list)):
        append_item(item_list[i])


############# Program entry point #################

# Initialize program
if not os.path.exists('user.txt'):
    with open('user.txt', 'a') as f:
        new_user = get_user('admin', 'none', 'admin', 'password')
        f.write(new_user.first_name + ',' + new_user.last_name + ',' + new_user.username + ',' + new_user.password)

if not os.path.exists('item.txt'):
    with open('item.txt', 'a') as f:
        f.write('')

# Read files and store into lists
user_list = []
with open('user.txt', 'r') as f:
    for line in f:
        temp = line.split(',')
        user = get_user(temp[0], temp[1], temp[2], temp[3].strip())
        user_list.append(user)

item_list = []
with open('item.txt', 'r') as f:
    for line in f:
        temp = line.split(',')
        item = get_item(temp[0], temp[1], temp[2], temp[3].strip())
        item_list.append(item)

logged_in = 0 # tracks log in status

def log_in():
    correct = 0
    while not correct:
        print('\nPlease Log In.')
        print('Enter username: ', end='')
        username = input()
        print('Enter password: ', end='')
        password = input()
        for i in range(0, len(user_list)):
            if user_list[i].username == username:
                if user_list[i].password == password:
                    correct = 1
                    break
        if not correct:
            print('Entered username and/or password are incorrect, please try again.')

    global logged_in
    logged_in = 1
    

def display_item():
    output = ''
    for i in range(0, len(item_list)):
        out_line = '%10s %10s %10s %10s\n'%(item_list[i].name, str(item_list[i].amount), item_list[i].unit, item_list[i].type)
        output += out_line
    display = Tk()
    display.title('Inventory')
    label = Label(display, text=output)
    label.pack()


def add_item():
    print('Enter item name: ', end='')
    name = input()
    print('Enter amount: ', end='')
    amount = int(input())
    print('Enter unit: ', end='')
    unit = input()
    print('Enter item type: ', end='')
    type = input()
    item = get_item(name, amount, unit, type)
    item_list.append(item)

def take_item():
    print('Enter item name: ', end='')
    name = input()
    print('Enter amount: ', end='')
    amount = int(input())
    index = -1
    for i in range(0, len(item_list)):
        if item_list[i].name == name:
            index = i
            break
    if index == -1:
        print(name + ' does not exists.')
    elif int(item_list[index].amount) < amount:
        print('Not enough inventory. Removing all of ' + name)
    else:
        item_list[index].amount = int(item_list[index].amount) - amount

def report():
    temp_list = []
    for i in range(0, len(item_list)):
        temp_list.append(item_list[i].type)
    graph = Tk()
    graph.title('Report')
    button = Button(graph, text="Generate Graph", command=lambda: plot(temp_list))
    button.pack()
    

def plot(list):
    plt.hist(list)
    plt.show()

def write_csv():
    list_of_list = []
    for i in range(0, len(item_list)):
        temp_list = [item_list[i].name, item_list[i].amount, item_list[i].unit, item_list[i].type]
        list_of_list.append(temp_list)
    df = pd.DataFrame(list_of_list)
    df.to_csv('out.csv', sep=';')

def log_out():
    global logged_in
    logged_in = 0


###### BEGIN ######
while 1:

    while not logged_in:
        log_in()

    print(
        '1) Display items\n' + 
        '2) Add item\n' + 
        '3) Take item\n' + 
        '4) Get Report\n' + 
        '5) Write to CSV\n' + 
        '6) Log out\n' +
        '7) Shut down\n' +
        'Select an option: '   
    )

    user_input = input()

    if user_input == '1':
        display_item()
    elif user_input == '2':
        add_item()
    elif user_input == '3':
        take_item()
    elif user_input == '4':
        report()
    elif user_input == '5':
        write_csv()
    elif user_input == '6':
        log_out()
    elif user_input == '7':
        write_user(user_list)
        write_item(item_list)
        break
    else:
        print('Wrong input, please try again.')


