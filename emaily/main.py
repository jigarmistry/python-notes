import requests
import datetime
from colorama import Fore, Back, Style
from tinydb import TinyDB, Query

db = TinyDB('db.json')

def get_menu():
    print (Fore.CYAN +"----------------------------")
    print (Fore.YELLOW +"1 : Show Your Previous Chats")
    print (Fore.YELLOW +"2 : Chat Now")
    print (Fore.YELLOW +"3 : Show Menu")
    print (Fore.YELLOW +"4 : Quit")
    print (Fore.CYAN +"----------------------------")


def handle_menu_option(option,person_name):
    if option == "4":
        print(Style.RESET_ALL)
        exit()
    elif option == "3":
        get_menu()
    elif option == "2":
        chat_now(person_name)
    elif option == "1":
        log_history()

def insert_into_db(data):
    db.insert(data)
    print (db.all())

def chat_now(person_name):
    print ("")
    print (Fore.WHITE +"Press Q For Exit From Chat")
    print (Fore.WHITE +"Press S For Show Current Chat")
    print ("")
    msg = "e"
    while msg != "Q":
        msg = input(Fore.GREEN + "Enter Your Message : "+ Fore.MAGENTA)
        datestamp = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        data = {'person':person_name,'msg':msg,'datestamp':datestamp}
        print (data)
        r = requests.post('http://127.0.0.1:8000/Emaily/default/getlogs.json', data = data)
        if r.status_code == 200 and msg != "S":
            insert_into_db(data)
        live_logs = r.json()
        print (live_logs)


def main():
    person_name = input(Fore.GREEN + "Enter Your Name : "+ Fore.MAGENTA)
    get_menu()
    while 1:
        option = input(Fore.GREEN + "Enter Your Option : "+ Fore.MAGENTA)
        handle_menu_option(option,person_name)
    print(Style.RESET_ALL)

main()
