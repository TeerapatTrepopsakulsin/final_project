import copy

import database
import csv

# define a function called initializing

def initializing():
    DB = database.Database()

    global persons
    persons = database.Table('persons')
    persons.insert('persons.csv')
    DB.insert(persons)

    global login_table
    login_table = database.Table('login')
    login_table.insert('login.csv')
    DB.insert(login_table)

    global project
    project = database.Table('project')
    project.insert('project.csv')
    DB.insert(project)

    global advisor_pending_request
    advisor_pending_request = database.Table('advisor_pending_request')
    advisor_pending_request.insert('advisor_pending_request.csv')
    DB.insert(advisor_pending_request)

    global member_pending_request
    member_pending_request = database.Table('member_pending_request')
    member_pending_request.insert('member_pending_request.csv')
    DB.insert(member_pending_request)



# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database
def identify(id):
    persons_list = copy.deepcopy(persons.table)
    for person in persons_list:
        if person['ID'] == id:
            return person['fist']
    return None


def isinproject(id ,project):
    if id == project['member1'] or val == project['member2'] or val == project['lead'] or val == project['advisor']:
        return True
    return False


# define a function called login

def login():
    username = input('Enter username: ')
    password = input('Enter password: ')
    for i in login_table.table:
        if username == i['username'] and password == i['password']:
            return [i['ID'], i['role']]
    return None


# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None

# define a function called exit
def exit():
    for i in [[persons,'persons.csv'],[login_table, 'login.csv'],[project, 'project.csv'], [advisor_pending_request, 'advisor_pending_request.csv'],[member_pending_request, 'member_pending_request.csv']]:
        my_file = open(i[1], 'w')
        writer = csv.writer(my_file)
        list_of_key = []
        if len(i[0].table) >= 1:
            for keys in i[0].table[0]:
                list_of_key.append(keys)
            writer.writerow(list_of_key)
            for dictionary in i[0].table:
                writer.writerow(dictionary.values())
        my_file.close()
    print('Logged out')


# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python

def student():
    print('Select your action')
    print('1. Requests')
    print('2. Create a project')
    print('3. Exit')
    choice = int(input('Input number(1-3): '))
    while choice != 3:
        if choice == 1:
            print(member_pending_request.table)
            print('Accept or Deny')
        elif choice == 2:
            print(project.table)
        choice = int(input('Input number(1-3): '))


def lead():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Responded requests')
    print('4. Send out members requests')
    print('5. Send out advisor requests')
    print('6. Request for project evaluation')
    print('7. Exit')
    choice = int(input('Input number(1-7): '))
    while choice != 7:
        if choice == 1:
            for _project in project.table:
                if isinproject(ID, _project):
                    print(_project)
        elif choice == 2:
            print(project.table)
            print('modify or not')
        elif choice == 3:
            print(member_pending_request.table)
        elif choice == 4:
            print(member_pending_request.table)
            print('send request 1 at a time')
            member_pending_request.update('member request')
        elif choice == 5:
            print(advisor_pending_request.table)
            print('send request 1 at a time')
            advisor_pending_request.update('advisor request')
        elif choice == 6:
            print(project.table)
            print('request confirm?')
            # change project status
            # cannot if already waiting for evaluation
        choice = int(input('Input number(1-7): '))


def member():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Responded requests')
    print('4. Exit')
    choice = int(input('Input number(1-4): '))
    while choice != 4:
        if choice == 1:
            for _project in project.table:
                if isinproject(ID, _project):
                    print(_project)
        elif choice == 2:
            print(project.table)
            print('modify or not')
        elif choice == 3:
            print(member_pending_request.table)
        choice = int(input('Input number(1-4): '))


def faculty():
    print('Select your action')
    print('1. Requests')
    print('2. See project status')
    print('3. Evaluate project')
    print('4. Approve project')
    print('5. Exit')
    choice = int(input('Input number(1-5): '))
    while choice != 5:
        if choice == 1:
            print(advisor_pending_request.table)
            print('Accept or Deny')
        elif choice == 2:
            print('Select your project type')
            print('1. Under advising project')
            print('2. Other project')
            print('3. Exit')
            choice = int(input('Input number(1-3): '))
            while choice != 3:
                if choice == 1:
                    for _project in project.table:
                        if isinproject(ID, _project):
                            print(_project)
                if choice == 2:
                    for _project in project.table:
                        if not isinproject(ID, _project):
                            print(_project)
                choice = int(input('Input number(1-3): '))
        elif choice == 3:
            print(project.table)
            print('pass or not')
        elif choice == 4:
            print(project.table)
            print('Approve or not')
        choice = int(input('Input number(1-5): '))


def admin():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. See pending members requests status')
    print('4. Modify pending members requests information')
    print('5. See pending advisor requests status')
    print('6. Modify pending advisor requests information')
    print('7. Exit')
    choice = int(input('Input number(1-7): '))
    while choice != 7:
        if choice == 1:
            for _project in project.table:
                print(_project)
        elif choice == 2:
            print(project.table)
            print('modify or not')
        elif choice == 3:
            print(member_pending_request.table)
        elif choice == 4:
            print(member_pending_request.table)
            print('modify or not')
        elif choice == 5:
            print(advisor_pending_request.table)
        elif choice == 6:
            print(advisor_pending_request.table)
            print('modify or not')
        choice = int(input('Input number(1-7): '))


        # make calls to the initializing and login functions defined above

initializing()
val = login()
while val is None:
    print('Invalid username or password.')
    print()
    val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
ID = copy.deepcopy(val[0])
role = copy.deepcopy(val[1])

if role == 'admin':
    admin()
elif role == 'student':
    student()
elif role == 'member':
    member()
elif role == 'lead':
    lead()
elif role == 'faculty' or role == 'advisor':
    faculty()

# once everything is done, make a call to the exit function

exit()

