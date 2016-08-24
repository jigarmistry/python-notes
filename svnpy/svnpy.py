import os
import sys
import argparse
import configparser

config = configparser.ConfigParser()
configtest = configparser.ConfigParser()
parser = argparse.ArgumentParser()

script_dir = os.path.dirname(__file__)
config.read(os.path.join(script_dir,"config.ini"))
configtest.read(os.path.join(script_dir,"configtest.ini"))
svn_username = "jigarm"

def string_color(color):
    ESC = "\x1b["
    END = "m"
    color_code = {
            "red": "1","green": "2","yellow": "3","blue": "4","magenta": "5",
            "cyan": "6","pink": "218"
            }
    code = ESC + "38;5;"
    ret_color = code + color_code[color] + END
    res_color = ESC + "0" + END
    return ret_color,res_color

def format_string(string,color):
    return "%s %s %s"%(string_color(color)[0],string,string_color('blue')[1])

def admin_actions():

    print("")
    print("1 : Add Project")
    print("2 : Edit Project")
    print("3 : Remove Project")
    print("4 : List Projects")
    print("5 : Exit")
    print("")

    while True:
        option = input("Enter Your Option : ")
        if option == "5":
            exit()
        elif option == "1":
            project_name = input("Enter Project Name : ")
            all_projects = dict(config.items('project_auth')).keys()
            if project_name in all_projects:
                print ("Project Already Exists")
                continue
            project_password = input("Enter Project Password : ")
            project_path = input("Enter Project Path : ")
            project_auth = config['project_auth']
            project_auth[project_name] = project_password
            project_path_et = config['project_path']
            project_path_et[project_name] = project_path
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print ("Project Added Successfully")
            print ("")
        elif option == "2":
            print ("edit")
        elif option == "3":
            project_name = input("Enter Project Name : ")
            all_projects = dict(config.items('project_auth')).keys()
            if project_name not in all_projects:
                print ("Project Not Exists")
                continue
            config.remove_option("project_auth",project_name)
            config.remove_option("project_path",project_name)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print ("Project Removed Successfully")
            print ("")
        elif option == "4":
            all_projects = dict(config.items('project_path'))
            print ("")
            for key,value in all_projects.items():
                print (format_string(key,"green") + " : "+value)
            print ("")


def set_arguments():
    parser.add_argument('-c', action='store', dest='svn_command',
                        help='SVN Command')
    parser.add_argument('-p', action='store', dest='project_name',
                        help='Name Of Project')
    parser.add_argument('-lp', action='store_true', dest='list_projects',
                        help='List Of Projects')
    parser.add_argument('-lc', action='store_true', dest='list_commands',
                        help='List Of Commands')
    parser.add_argument('-admin', action='store_true', dest='admin',
                        help='Admin Actions')


def get_list_projects(option):
    dict_projects = dict(config.items('project_auth'))
    if option == 1:
        print ("----------")
        print ("Projects : ")
        print ("----------")
        for key in dict_projects.keys():
            print (key)
        print ("")
    return dict_projects.keys()


def get_list_commands(option):
    list_commands = ["up", "st", "commit", "info", "log", "list"]
    list_commands += ["cleanup", "delete", "upwithr","add"]
    if option == 1:
        print ("----------")
        print ("Commands : ")
        print ("----------")
        for command in list_commands:
            print (command)
        print ("")
    return list_commands


def get_file_names(str_file_names):
    file_names = str_file_names.split(",")
    print(file_names)
    str_final = ""
    for filename in file_names:
        filename = filename.replace(" ","\ ")
        str_final += filename + " "
    return str_final


def handle_command(svn_command, auth_string):
    if svn_command in ["up","st","info","cleanup","log"]:
        os.system("svn %s"%(svn_command) + auth_string)
    if svn_command == "upwithr":
        str_rev_name = input("Enter Revision : ")
        os.system("svn up -r %s" % (str_rev_name) + auth_string)
    if svn_command == "delete":
        str_file_names = input("Enter File Names (filename1,filename2) : ")
        os.system("svn delete %s" % (get_file_names(str_file_names)) + auth_string)
    if svn_command == "add":
        str_file_names = input("Enter File Names (filename1,filename2) : ")
        print(get_file_names(str_file_names))
        os.system("svn add %s" % (get_file_names(str_file_names)) + auth_string)
    if svn_command == "list":
        check = input("File Name? (y/n) : ")
        str_file_names = ""
        if check == "y":
            str_file_names = input("Enter File Name (filename1) : ")
        os.system("svn list -v %s"%(get_file_names(str_file_names)) + auth_string)
    if svn_command == "commit":
        commit_msg = input("Enter Commit Message : ")
        check = input("File Names? (y/n) : ")
        str_file_names = ""
        if check == "y":
            str_file_names = input("Enter File Names (filename1,filename2) : ")
        os.system("svn commit -m '%s' %s" % (commit_msg, get_file_names(str_file_names)) + auth_string)


def execute_command(project_name, svn_command):
    all_projects = get_list_projects(2)
    if project_name in all_projects:
        project_path = config['project_path'][project_name]
        os.chdir(project_path)
        project_auth = config['project_auth'][project_name]
        auth_string = " --username %s --password %s" % (svn_username,project_auth)
        all_commands = get_list_commands(2)
        if svn_command in all_commands:
            handle_command(svn_command, auth_string)
        else:
            print ("No Command Found : ", svn_command)
    else:
        print ("No Project Found : ", project_name)


def main():
    set_arguments()
    results = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    if results.admin:
        admin_actions()
        sys.exit(1)
    if results.list_projects:
        get_list_projects(1)
        sys.exit(1)
    if results.list_commands:
        get_list_commands(1)
        sys.exit(1)
    if results.svn_command and results.project_name:
        execute_command(results.project_name, results.svn_command)
    else:
        print ("Please specify command with -c argument")

main()
