import requests
import datetime
from colorama import Fore, Back, Style
from tinydb import TinyDB, Query

db = TinyDB('db.json')
#remote_api = "127.0.0.1:8000"
remote_api = "pythonui.pythonanywhere.com"

def check_internet_connection():
    try:
        r = requests.get("http://info.cern.ch")
        return True
    except Exception as e:
        return False

def get_menu():
    print (Fore.CYAN +"----------------------------")
    print (Fore.YELLOW +"1 : Show Your Previous Chats")
    print (Fore.YELLOW +"2 : Chat Now")
    print (Fore.YELLOW +"3 : Show Menu")
    print (Fore.YELLOW +"4 : Quit")
    print (Fore.CYAN +"----------------------------")

def handle_menu_option(option,person_name):
    if option == "4":
        print ("")
        print (Fore.WHITE + "Thank You..")
        print(Style.RESET_ALL)
        exit()
    elif option == "3":
        get_menu()
    elif option == "2":
        chat_now(person_name)
    elif option == "1":
        print_logs(db.table(person_name).all())

def insert_into_db(data,person_name):
    table = db.table(person_name)
    table.insert(data)

def verify_user(person_name):
    data = {'person':person_name}
    r = requests.post('http://'+remote_api+'/Emaily/default/getusers.json', data = data)
    result = r.json()
    return result

def print_logs(live_logs):
    logs = live_logs
    print ("")
    for log in reversed(logs):
        datestamp = str(log["datestamp"])[12:]
        print (Fore.CYAN + str(log["person"]) + " (" +str(datestamp) + ")"+" : " + Fore.MAGENTA + str(log["msg"]))
    print ("")

def chat_now(person_name):
    print ("")
    print (Fore.WHITE +"Press Q For Exit From Chat")
    print (Fore.WHITE +"Press S For Show Current Chat")
    print (Fore.WHITE +"Press H For Hide Current Chat")
    print ("")
    msg = "e"
    while msg != "Q":
        msg = input(Fore.GREEN + "Enter Your Message : "+ Fore.MAGENTA)
        if msg == "Q":
            get_menu()
            break
        if msg == "":
            continue
        if msg == "H":
            import os
            os.system('cls' if os.name=='nt' else 'clear')
            continue
        datestamp = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        data = {'person':person_name,'msg':msg,'datestamp':datestamp}
        r = requests.post('http://'+remote_api+'/Emaily/default/getlogs.json', data = data)
        if r.status_code == 200 and msg != "S" and msg != "H":
            insert_into_db(data,person_name)
        live_logs = r.json()
        print_logs(live_logs["logs"])

def main():
    person_name = input(Fore.GREEN + "Enter Your Name : "+ Fore.MAGENTA)
    is_internet = check_internet_connection()
    if is_internet:
        result = verify_user(person_name)
        if result["login"] == "yes":
            print ("")
            print (Fore.WHITE + "Welcome " + person_name + ", " + result["msg"])
        else:
            print (Fore.RED +result["msg"])
            print (Fore.RED +"Exit")
            print(Style.RESET_ALL)
            exit()
        get_menu()
        while 1:
            option = input(Fore.GREEN + "Enter Your Option : "+ Fore.MAGENTA)
            handle_menu_option(option,person_name)
        print(Style.RESET_ALL)
    else:
        print (Fore.RED + "Internet Connection Is Not Available")

main()
