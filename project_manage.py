import copy
import random
import sys
import database
import csv
from time import time, strftime, localtime

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
            return f"{person['fist']} {person['last']}"
    return None


def int_autocorrect(num, a):
    if isinstance(num, int):
        return num
    return a


def isinproject(id, project):
    if id in project.values():
        return True
    return False


def count_requests(table, id):
    count = 0
    for request in table:
        if isinproject(id, request) and request['response'] == '':
            count += 1
    return count


def confirm():
    print()
    print('Press only Enter to Confirm')
    choice = input('Press other key to Cancel ')
    if choice == "":
        return True
    return False


def create_project_id():
    exist_id = [i['ID'] for i in project.table]
    selected_id = random.sample([str(i) for i in range(100000, 999999) if str(i) not in exist_id], 1)
    return selected_id


def admin_modify(self):
    for request in self.table:
        print(request)
    project_id = input('Input project ID to modify ')
    attribute = input('Input attribute that you want to modify ')
    print(f'{project_id} {attribute} is currently {self.get_row(project_id, attribute)}.')
    new_value = input('Insert new value ')
    print('Do you want to modify?')
    if confirm():
        self.set_row(project_id, attribute, new_value)
        print('Modifying completed')
    else:
        print('Modifying canceled')


class Project:
    def __init__(self, ID):
        self.ID = ID
        self.title = project.get_row(ID, 'title')
        self.lead = project.get_row(ID, 'lead')
        self.member1 = project.get_row(ID, 'member1')
        self.member2 = project.get_row(ID, 'member2')
        self.advisor = project.get_row(ID, 'advisor')
        self.status = project.get_row(ID, 'status')
        #self.__dict__ = {'ID':self.ID,'title':self.title,'lead':self.lead,'member1':self.member1,'member2':self.member2,'advisor':self.advisor,'status':self.status}

    def show(self):
        print(f'Project title: {self.title}\n'
                f'Lead: {identify(self.lead)}\n'
                f'Member: {identify(self.member1)}\n'
                f'Member: {identify(self.member2)}\n'
                f'Advisor: {identify(self.advisor)}\n'
                f'Project status: {self.status}')

    def show_request(self):
        print('--Request history--')
        for table in [member_pending_request.table, advisor_pending_request.table]:
            for i in table:
                if i['ID'] == self.ID:
                    if i['response'] == '':
                        print(f"{identify(i['member'])} hasn't responded to the request")
                    else:
                        print(f"{identify(i['member'])} had {i['response']} the request on {i['response_date']}")

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
    print()
    while choice != 3:
        if choice == 1:
            k = 0
            for request in member_pending_request.table:
                if isinproject(ID, request) and request['response'] == '' and k == 0:
                    project_id = copy.deepcopy(request['ID'])
                    your_project = Project(project_id)
                    print(f'{identify(your_project.lead)} want you to join {your_project.title} project.')
                    your_project.show()
                    k += 1
            if k == 0:
                print('You have no request')
            else:
                print()
                print('Select your action')
                print('1. Accept')
                print('2. Deny')
                print('3. Cancel')
                choice = int(input('Input number(1-3): '))
                print()
                if choice == 1:
                    print('Are you sure? (Accept)')
                    if confirm():
                        if your_project.member1 == '':
                            project.set_row(project_id, 'member1', ID)
                        elif your_project.member2 == '':
                            project.set_row(project_id, 'member2', ID)
                        # become member
                        member_pending_request.set_row(project_id, 'response', 'Accepted').set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time())))
                        # member_request update
                        login_table.set_row(ID, 'role', 'member')
                        exit()
                        sys.exit('Changing you role to Member. Automatic Logout')
                        # login update
                    else:
                        print('Accepting canceled')
                elif choice == 2:
                    print('Are you sure? (Deny)')
                    if confirm():
                        member_pending_request.set_row(project_id, 'response', 'Denied').set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time())))
                        # member_request update
                        print('Denying confirmed')
                    else:
                        print('Denying canceled')
        elif choice == 2:
            title = str(input('Please insert the project title: '))
            print('Do you want to create a project')
            if confirm():
                new_project_id = create_project_id()
                new_project = {'ID': new_project_id[0],
                               'title': title,
                               'lead': ID,
                               'member1': None,
                               'member2': None,
                               'advisor': None,
                               'status': 'Not started'}
                project.table.append(new_project)
                login_table.set_row(ID, 'role', 'lead')
                exit()
                sys.exit('Changing you role to Lead. Automatic Logout')
            else:
                print('Creating canceled')
        print()
        print('Select your action')
        print('1. Requests')
        print('2. Create a project')
        print('3. Exit')
        choice = int(input('Input number(1-3): '))
        print()


def lead():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Requests history')
    print('4. Send out members requests')
    print('5. Send out advisor requests')
    print('6. Request for project evaluation')
    print('7. Exit')
    choice = int(input('Input number(1-7): '))
    print()
    while choice != 7:
        if choice == 1:
            for _project in project.table:
                if isinproject(ID, _project):
                    project_id = copy.deepcopy(_project['ID'])
                    your_project = Project(project_id)
                    your_project.show()
        elif choice == 2:
            print(project.table)
            print('modify or not')
        elif choice == 3:
            for _project in project.table:
                if isinproject(ID, _project):
                    project_id = copy.deepcopy(_project['ID'])
                    your_project = Project(project_id)
                    your_project.show_request()
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
        print()
        print('Select your action')
        print('1. See project status')
        print('2. Modify project information')
        print('3. Requests history')
        print('4. Send out members requests')
        print('5. Send out advisor requests')
        print('6. Request for project evaluation')
        print('7. Exit')
        choice = int(input('Input number(1-7): '))
        print()


def member():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Requests history')
    print('4. Exit')
    choice = int(input('Input number(1-4): '))
    print()
    while choice != 4:
        if choice == 1:
            for _project in project.table:
                if isinproject(ID, _project):
                    project_id = copy.deepcopy(_project['ID'])
                    your_project = Project(project_id)
                    your_project.show()
        elif choice == 2:
            print(project.table)
            print('modify or not')
        elif choice == 3:
            for _project in project.table:
                if isinproject(ID, _project):
                    project_id = copy.deepcopy(_project['ID'])
                    your_project = Project(project_id)
                    your_project.show_request()
        print()
        print('Select your action')
        print('1. See project status')
        print('2. Modify project information')
        print('3. Requests history')
        print('4. Exit')
        choice = int(input('Input number(1-4): '))
        print()


def faculty():
    print('Select your action')
    print('1. Requests')
    print('2. See project status')
    print('3. Evaluate project')
    print('4. Approve project')
    print('5. Exit')
    choice = int(input('Input number(1-5): '))
    print()
    while choice != 5:
        if choice == 1:
            print(advisor_pending_request.table)
            print('Accept or Deny')
        elif choice == 2:
            print('Select your project type')
            print('1. Under advising project')
            print('2. Other project')
            print('3. Cancel')
            choice = int(input('Input number(1-3): '))
            print()
            while choice != 3:
                if choice == 1:
                    for _project in project.table:
                        if isinproject(ID, _project):
                            project_id = copy.deepcopy(_project['ID'])
                            your_project = Project(project_id)
                            your_project.show()
                elif choice == 2:
                    for _project in project.table:
                        if not isinproject(ID, _project):
                            print(_project)
                choice = int(input('Input number(1-3): '))
                print()
        elif choice == 3:
            print(project.table)
            print('pass or not')
        elif choice == 4:
            print(project.table)
            print('Approve or not')
        print()
        print('Select your action')
        print('1. Requests')
        print('2. See project status')
        print('3. Evaluate project')
        print('4. Approve project')
        print('5. Exit')
        choice = int(input('Input number(1-5): '))
        print()


def admin():
    print('Select your action')
    print('1. See project data')
    print('2. Modify project data')
    print('3. See pending members data')
    print('4. Modify pending members requests data')
    print('5. See pending advisor requests data')
    print('6. Modify pending advisor requests data')
    print('7. Exit')
    choice = int(input('Input number(1-7): '))
    print()
    while choice != 7:
        if choice == 1:
            for _project in project.table:
                print(_project)
        elif choice == 2:
            table = copy.deepcopy(project)
            admin_modify(table)
        elif choice == 3:
            for request in member_pending_request.table:
                print(request)
        elif choice == 4:
            table = copy.deepcopy(member_pending_request)
            admin_modify(table)
        elif choice == 5:
            for request in advisor_pending_request.table:
                print(request)
        elif choice == 6:
            table = copy.deepcopy(advisor_pending_request)
            admin_modify(table)
        print()
        print('Select your action')
        print('1. See project data')
        print('2. Modify project data')
        print('3. See pending members data')
        print('4. Modify pending members requests data')
        print('5. See pending advisor requests data')
        print('6. Modify pending advisor requests data')
        print('7. Exit')
        choice = int(input('Input number(1-7): '))
        print()


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
# project1 = {'ID':'1234567','title':'colourblind','lead':'1235567','member1':'1234568','member2':None,'advisor':'1234888','status':'nothing'}
# pending_member1 = {'ID':'1234567','member':'2235567','response':False,'response_date':None}
# project.table.append(project1)
# member_pending_request.table.append(pending_member1)
# print(Project('1234567').show())
# print(count_requests(member_pending_request.table, '0000000'))
# print(Project('1234567').__dict__)
# for i in project.table:
#     if i['ID'] == '2023341':
#         i.update({'ID': '2023341', 'title': 'colourblind', 'lead': '1235567', 'member1': '1234568', 'member2': '0000000', 'advisor': '1234888', 'status': 'nothing'})
# login_table.set_row('0000000','password','5').set_row('0000000','username','4').set_row('1234567', 'response', 'Denied').
# member_pending_request.set_row('1234567', 'response_date',strftime("%d/%b/%Y", localtime(time())))

exit()

