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
        # print(i[0].table)
        for keys in i[0].table[0]:
            list_of_key.append(keys)
        writer.writerow(list_of_key)
        for dictionary in i[0].table:
            writer.writerow(dictionary.values())
        my_file.close()


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


def lead():
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Responded requests')
    print('4. Send out members requests')
    print('5. Send out advisor requests')
    print('6. Exit')
    choice = int(input('Input number(1-6): '))
    while choice != 6:
        if choice == 1:
            print(project.table)
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


        # make calls to the initializing and login functions defined above

initializing()
val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities

# once everything is done, make a call to the exit function
exit()
