import copy
import sys
import csv
from random import sample
from time import time, strftime, localtime
import database


def initializing():
    """
    create an object to read all csv files that will serve as a persistent state for this program,
    then create all the corresponding tables for those csv files,
    and add all these tables to the database
    """
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


def identify(person_id):
    """
    convert person ID into their name (First name, Last name)
    :param person_id:
    :return: str of the name of the person, None if invalid
    """
    persons_list = copy.deepcopy(persons.table)
    for person in persons_list:
        if person['ID'] == person_id:
            return f"{person['first']} {person['last']}"
    return None


def isinproject(any_id, project):
    """
    check if the ID is in the project or not
    :param any_id: str of ID
    :param project: dict with project status
    :return: True if the ID is in the project, False otherwise
    """
    if any_id in project.values():
        return True
    return False


def count_project(any_id):
    """
    count the number of projects that the person with specific ID is in
    :param any_id: str of ID
    :return: int of the number of projects
    """
    count = 0
    for _project in project.table:
        if isinproject(any_id, _project):
            count += 1
    return count


def count_requests(self, any_id):
    """
    count the number of pending requests of the specific ID in specific table
    :param self: name of csv file
    :param any_id: str of ID
    :return: int of the number of pending requests
    """
    count = 0
    for request in self.table:
        if isinproject(any_id, request) and request['response'] == '':
            count += 1
    return count


def member_auto_deny(member_id):
    """
    deny all request when become member of the project
    :param member_id: str of member ID
    """
    for request in member_pending_request.filter(lambda x: x['response'] == '' and x['member'] == member_id).table:
        (member_pending_request.set_row(request['ID'], 'response', 'Denied')
         .set_row(request['ID'], 'response_date', strftime("%d/%b/%Y", localtime(time()))))


def advisor_auto_deny(advisor_id):
    """
    deny all request when become advisor of 5 projects
    :param advisor_id: str of advisor ID
    """
    if count_project(advisor_id) == 5:
        for request in advisor_pending_request.filter(lambda x: x['response'] == '' and x['advisor'] == advisor_id).table:
            (advisor_pending_request.set_row(request['ID'], 'response', 'Denied')
             .set_row(request['ID'], 'response_date', strftime("%d/%b/%Y", localtime(time()))))


def request_auto_invalid(project_id):
    """
    request become invalid if and only if project is in progress or project member is full
    :param project_id: str of project ID
    """
    your_project = Project(project_id)
    if your_project.status not in ('Not started', 'Initiate', 'Planned') or your_project.member2 not in (None, ''):
        for request in member_pending_request.filter(lambda x: x['response'] == '' and x['ID'] == your_project.ID).table:
            member_pending_request.set_row(your_project.ID, 'response', 'Invalid').set_row(request['ID'], 'response_date',
                                                                                        strftime("%d/%b/%Y",
                                                                                                 localtime(time())))


def call_project_id(person_id):
    """
    convert person ID into a list of project ID which the person is in.
    can only use for project.csv
    :param person_id: str of person ID
    :return: list of str of project ID
    """
    project_id_list = []
    for _project in project.table:
        if isinproject(person_id, _project):
            project_id = copy.deepcopy(_project['ID'])
            project_id_list.append(project_id)
    return project_id_list


def isinrequest(project_id, person_id):
    """
    check whether the person with specific ID have the request history
    with project with specific ID or not
    :param project_id: str of project ID
    :param person_id: str of person ID
    :return: True if have, False otherwise
    """
    for table in member_pending_request.table, advisor_pending_request.table:
        for request in table:
            if request['ID'] == project_id and isinproject(person_id, request):
                return True
    return False


def show_person(role_list, exclude_project_id):
    """
    show person ID, name and role which have the same role as in the role list
    and doesn't be part of specific excluded project ID and available for other project
    :param role_list: list of roles
    :param exclude_project_id: str of project ID
    :return: list of person ID which has showed
    """
    available_id = []
    for person in login_table.table:
        if (person['role'] in role_list and not isinrequest(exclude_project_id, person['ID']) and
                len(call_project_id(person['ID'])) < 5):
            print(f"{person['ID']:^9} | {identify(person['ID']):<18} | Role: {person['role']}")
            available_id.append(person['ID'])
    return available_id


def confirm():
    """
    ask to confirm, will return True if confirmed, False otherwise
    :return: True if confirmed, False otherwise
    """
    print()
    print('Press only Enter to Confirm')
    choice = input('Press other key to Cancel ')
    if choice == "":
        return True
    return False


def create_project_id():
    """
    create new project ID which is str of 6 digits number and doesn't already exist
    :return: str of project ID
    """
    exist_id = [i['ID'] for i in project.table]
    selected_id = sample([str(i) for i in range(100000, 999999) if str(i) not in exist_id], 1)
    return selected_id


def admin_modify(self):
    """
    function for admin role, especially modifying each table data
    :param self: name of csv file
    """
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


##############################################################################
class Project:
    def __init__(self, ID):
        self.ID = ID
        self.title = project.get_row(ID, 'title')
        self.lead = project.get_row(ID, 'lead')
        self.member1 = project.get_row(ID, 'member1')
        self.member2 = project.get_row(ID, 'member2')
        self.advisor = project.get_row(ID, 'advisor')
        self.status = project.get_row(ID, 'status')
        self.proposal = project.get_row(ID, 'proposal')
        self.report = project.get_row(ID, 'report')

    def update(self):
        project.update(self.ID, self.__dict__)

    def show(self):
        print(f'Project title: {self.title}\n'
                f'Lead: {identify(self.lead)}\n'
                f'Member: {identify(self.member1)}\n'
                f'Member: {identify(self.member2)}\n'
                f'Advisor: {identify(self.advisor)}\n'
                f'Project status: {self.status}')

    def show_request(self):
        print('--Request history--')
        k = 0
        for table in [member_pending_request.table, advisor_pending_request.table]:
            for i in table:
                if i['ID'] == self.ID:
                    if k == 0:
                        if i['response'] in ('', 'Invalid'):
                            print(f"{identify(i['member'])} hasn't responded to the member request")
                        else:
                            print(f"{identify(i['member'])} had {i['response']} "
                                  f"the member request on {i['response_date']}")
                    elif k == 1:
                        if i['response'] in ('', 'Invalid'):
                            print(f"{identify(i['advisor'])} hasn't responded to the advisor request")
                        else:
                            print(f"{identify(i['advisor'])} had {i['response']} "
                                  f"the advisor request on {i['response_date']}")
            k += 1

    def show_proposal(self, member_or_faculty='member'):
        if member_or_faculty == 'member':
            print('---Proposal---')
            print(self.proposal)
        else:
            if self.status in ['Not started', 'Initiate']:
                print("Lead of this project hasn't submit any proposal.")
            elif self.status == 'Planned':
                print('---Proposal---')
                print(self.proposal)
                print('This project proposal has not been approved.')
            else:
                print('---Proposal---')
                print(self.proposal)
                print('This project proposal is approved.')

    def show_report(self, member_or_faculty='member'):
        if member_or_faculty == 'member':
            print('---Report---')
            print(self.report)
        else:
            if self.status in ('Not started', 'Initiate', 'Planned', 'In progress'):
                print("Lead of this project hasn't submit any report.")
            elif self.status == 'Reported':
                print('---Report---')
                print(self.report)
                print('This project report has not been approved.')
            elif self.status == 'Advisor-approved':
                print('---Report---')
                print(self.report)
                print('This project report is waiting for another faculty to approve')
            else:
                print('---Report---')
                print(self.report)
                print('This project report is approved.')

    def modify(self):
        if self.status in ('Not started', 'Initiate', 'Planned'):
            print('Select your action')
            print('1. Change project title')
            print('2. Modify project proposal')
            print('3. Cancel')
            choice = input('Input number(1-3): ')
            print()
            if choice == '1':
                print(f'Current project title: {self.title}')
                new_title = input('Insert new title ')
                print('Do you want to change?')
                if confirm():
                    self.title = new_title
                    self.update()
                    print('Modifying completed')
                else:
                    print('Modifying canceled')
            elif choice == '2':
                self.show_proposal()
                print()
                new_proposal = input('Insert new proposal ')
                print('Do you want to modify?')
                if confirm():
                    self.proposal = new_proposal
                    self.update()
                    print('Modifying completed')
                else:
                    print('Modifying canceled')
        else:
            print('1. Modify project report')
            print('2. Cancel')
            choice = input('Input number(1-2): ')
            print()
            if choice == '1':
                self.show_report()
                print()
                new_report = input('Insert new report ')
                print('Do you want to modify?')
                if confirm():
                    self.report = new_report
                    self.update()
                    print('Modifying completed')
                else:
                    print('Modifying canceled')


##############################################################################
def login():
    """
    ask a user for a username and password
    :return: [ID, role] if valid, None otherwise
    """
    username = input('Enter username: ')
    password = input('Enter password: ')
    for i in login_table.table:
        if username == i['username'] and password == i['password']:
            return [i['ID'], i['role']]
    return None


def exit():
    """  write out all the tables that have been modified to the corresponding csv files """
    for i in [[persons, 'persons.csv'], [login_table, 'login.csv'], [project, 'project.csv'],
              [advisor_pending_request, 'advisor_pending_request.csv'],
              [member_pending_request, 'member_pending_request.csv']]:
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


def student():
    """ function for student role """
    print('Select your action')
    print('1. Requests')
    print('2. Create a project')
    print('3. Exit')
    choice = input('Input number(1-3): ')
    print()
    while choice != '3':
        if choice == '1':
            k = 0
            for request in member_pending_request.table:
                if isinproject(ID, request) and request['response'] == '' and k == 0:
                    project_id = copy.deepcopy(request['ID'])
                    your_project = Project(project_id)
                    n_request = count_requests(member_pending_request, ID)
                    if n_request >= 2:
                        print(f"You have {identify(your_project.lead)}'s and "
                              f"{n_request - 1} other requests pending.")
                    else:
                        print(f"You have {identify(your_project.lead)}'s request pending.")
                    print(f'{identify(your_project.lead)} want you to '
                          f'join {your_project.title} project.')
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
                choice = input('Input number(1-3): ')
                print()
                if choice == '1':
                    print('Are you sure? (Accept)')
                    if confirm():
                        if your_project.member1 == '':
                            your_project.member1 = ID
                            # project.set_row(project_id, 'member1', ID)
                        elif your_project.member2 == '':
                            your_project.member2 = ID
                            # project.set_row(project_id, 'member2', ID)
                        your_project.update()
                        # become member
                        member_pending_request.set_row(project_id, 'response', 'Accepted').set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time())))
                        member_auto_deny(ID)
                        request_auto_invalid(project_id)
                        # member_request update
                        login_table.set_row(ID, 'role', 'member')
                        exit()
                        sys.exit('Changing you role to Member. Automatic Logout')
                        # login update
                    else:
                        print('Accepting canceled')
                elif choice == '2':
                    print('Are you sure? (Deny)')
                    if confirm():
                        (member_pending_request.set_row(project_id, 'response', 'Denied')
                         .set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time()))))
                        # member_request update
                        print('Denying confirmed')
                    else:
                        print('Denying canceled')
        elif choice == '2':
            title = str(input('Please insert the project title: '))
            print('Do you want to create a project')
            if confirm():
                member_auto_deny(ID)
                new_project_id = create_project_id()
                new_project = {'ID': new_project_id[0],
                               'title': title,
                               'lead': ID,
                               'member1': '',
                               'member2': '',
                               'advisor': '',
                               'status': 'Not started',
                               'proposal': '',
                               'report': ''}
                project.table.append(new_project)
                login_table.set_row(ID, 'role', 'lead')
                exit()
                sys.exit('Changing you role to Lead. Automatic Logout')
            else:
                print('Creating canceled')
        else:
            print('Incorrect input. Try again')
        print()
        print('Select your action')
        print('1. Requests')
        print('2. Create a project')
        print('3. Exit')
        choice = input('Input number(1-3): ')
        print()


def lead():
    """ function for lead role """
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Requests history')
    print('4. Send out members requests')
    print('5. Send out advisor requests')
    print('6. Cancel members requests')
    print('7. Cancel advisor requests')
    print('8. Request for project evaluation')
    print('9. Exit')
    choice = input('Input number(1-9): ')
    print()
    while choice != '9':
        if choice == '1':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.show()
                your_project.show_proposal()
                your_project.show_report()
        elif choice == '2':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.modify()
        elif choice == '3':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.show_request()
        elif choice == '4':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                if count_requests(member_pending_request, your_project.ID) >= 3:
                    print('Pending requests reach limit.')
                elif your_project.status not in ('Not started', 'Initiate', 'Planned'):
                    print('Your project already in progress.')
                elif your_project.member2 not in (None, ''):
                    print('Members reach limit.')
                else:
                    print('Available students')
                    print()
                    available_id = show_person(['student'], project_id)
                    print()
                    while True:
                        member_id = input('Insert ID of the person you want: ')
                        if member_id in available_id:
                            break
                        print('Incorrect ID. Please try again')
                    print('Are you sure to send a request?')
                    if confirm():
                        new_request = {'ID': project_id,
                                       'member': member_id,
                                       'response': '',
                                       'response_date': ''}
                        member_pending_request.table.append(new_request)
                        print('Sending confirmed')
                    else:
                        print('Sending canceled')
            # can't send if project in_progress or already 2 members or 3 requests
        elif choice == '5':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                if count_requests(advisor_pending_request, your_project.ID) >= 1:
                    print('Pending requests reach limit.')
                elif your_project.advisor not in (None, ''):
                    print('Advisor reach limit.')
                else:
                    print('Available faculties')
                    print()
                    available_id = show_person(['faculty', 'advisor'], project_id)
                    # not over 5
                    print()
                    while True:
                        advisor_id = input('Insert ID of the faculty you want to be supervised: ')
                        if advisor_id in available_id:
                            break
                        print('Incorrect ID. Please try again')
                    print('Are you sure to send a request?')
                    if confirm():
                        new_request = {'ID': project_id,
                                       'advisor': advisor_id,
                                       'response': '',
                                       'response_date': ''}
                        advisor_pending_request.table.append(new_request)
                        print('Sending confirmed')
                    else:
                        print('Sending canceled')
            # can't send if 1 advisor or 1 request
        elif choice == '6':
            project_id = call_project_id(ID)[0]
            if count_requests(member_pending_request, project_id) <= 0:
                print('You have no member pending request')
            else:
                print('Pending member request')
                print()
                available_id = []
                for request in member_pending_request.table:
                    if isinproject(project_id, request) and request['response'] == '':
                        print(f"{request['member']:^9} | "
                              f"{identify(request['member']):<18} | "
                              f"Waiting...")
                        available_id.append(request['member'])
                print()
                while True:
                    member_id = input('Insert ID of the person you want to cancel: ')
                    if member_id in available_id:
                        break
                    print('Incorrect ID. Please try again')
                print('Are you sure to cancel the request?')
                if confirm():
                    member_pending_request.table.remove({
                        'ID': project_id,
                        'member': member_id,
                        'response': '',
                        'response_date': ''})
                    print('Cancelling confirmed')
                else:
                    print('Cancelling canceled')
        # cancel members requests
        elif choice == '7':
            project_id = call_project_id(ID)[0]
            if count_requests(advisor_pending_request, project_id) <= 0:
                print('You have no advisor pending request')
            else:
                print('Pending advisor request')
                print()
                available_id = []
                for request in advisor_pending_request.table:
                    if isinproject(project_id, request) and request['response'] == '':
                        print(f"{request['advisor']:^9} | "
                              f"{identify(request['advisor']):<18} | "
                              f"Waiting...")
                        available_id.append(request['advisor'])
                print()
                while True:
                    advisor_id = input('Insert ID of the faculty you want to cancel: ')
                    if advisor_id in available_id:
                        break
                    print('Incorrect ID. Please try again')
                print('Are you sure to cancel the request?')
                if confirm():
                    advisor_pending_request.table.remove(
                        {'ID': project_id,
                         'advisor': advisor_id,
                         'response': '',
                         'response_date': ''})
                    print('Cancelling confirmed')
                else:
                    print('Cancelling canceled')
        # Cancel advisor requests
        elif choice == '8':
            project_id = call_project_id(ID)[0]
            your_project = Project(project_id)
            if your_project.status == 'Initiate':
                your_project.show_proposal()
                print('Are you sure to send the request? (Proposal evaluation)')
                if confirm():
                    your_project.status = 'Planned'
                    your_project.update()
                    # change project status
                    print('Sending canceled')
                else:
                    print('Sending canceled')
            elif your_project.status == 'In progress':
                your_project.show_report()
                print('Are you sure to send the request? (Report evaluation)')
                if confirm():
                    your_project.status = 'Reported'
                    your_project.update()
                    # change project status
                    print('Sending canceled')
                else:
                    print('Sending canceled')
            elif your_project.status == 'Not started':
                print('Project has no advisor.')
            elif your_project.status in ('Planned', 'Reported'):
                print('The request is already sent.')
            else:
                print('Cannot send any more report.')
            # cannot if already waiting for evaluation
        else:
            print('Incorrect input. Try again')
        print()
        print('Select your action')
        print('1. See project status')
        print('2. Modify project information')
        print('3. Requests history')
        print('4. Send out members requests')
        print('5. Send out advisor requests')
        print('6. Cancel members requests')
        print('7. Cancel advisor requests')
        print('8. Request for project evaluation')
        print('9. Exit')
        choice = input('Input number(1-9): ')
        print()


def member():
    """ function for member role """
    print('Select your action')
    print('1. See project status')
    print('2. Modify project information')
    print('3. Requests history')
    print('4. Exit')
    choice = input('Input number(1-4): ')
    print()
    while choice != '4':
        if choice == '1':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.show()
                your_project.show_proposal()
                your_project.show_report()
        elif choice == '2':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.modify()
        elif choice == '3':
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                your_project.show_request()
        else:
            print('Incorrect input. Try again')
        print()
        print('Select your action')
        print('1. See project status')
        print('2. Modify project information')
        print('3. Requests history')
        print('4. Exit')
        choice = input('Input number(1-4): ')
        print()


def faculty():
    """ function for faculty role """
    print('Select your action')
    print('1. Requests')
    print('2. See project status')
    print('3. Evaluate project')
    print('4. Approve project')
    print('5. Exit')
    choice = input('Input number(1-5): ')
    print()
    while choice != '5':
        if choice == '1':
            k = 0
            for request in advisor_pending_request.table:
                if isinproject(ID, request) and request['response'] == '' and k == 0:
                    project_id = copy.deepcopy(request['ID'])
                    your_project = Project(project_id)
                    n_request = count_requests(advisor_pending_request, ID)
                    if n_request >= 2:
                        print(f"You have {identify(your_project.lead)}'s and "
                              f"{n_request - 1} other requests pending.")
                    else:
                        print(f"You have {identify(your_project.lead)}'s request pending.")
                    print(f'{identify(your_project.lead)} want you to '
                          f'supervise {your_project.title} project.')
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
                choice = input('Input number(1-3): ')
                print()
                if choice == '1':
                    print('Are you sure? (Accept)')
                    if confirm():
                        your_project.advisor = ID
                        your_project.status = 'Initiate'
                        your_project.update()
                        # become advisor
                        (advisor_pending_request.set_row(project_id, 'response', 'Accepted')
                         .set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time()))))
                        advisor_auto_deny(ID)
                        # advisor_request update
                        login_table.set_row(ID, 'role', 'advisor')
                        # login update
                        print('Accepting confirmed')
                    else:
                        print('Accepting canceled')
                elif choice == '2':
                    print('Are you sure? (Deny)')
                    if confirm():
                        (advisor_pending_request.set_row(project_id, 'response', 'Denied')
                         .set_row(project_id, 'response_date', strftime("%d/%b/%Y", localtime(time()))))
                        # advisor_request update
                        print('Denying confirmed')
                    else:
                        print('Denying canceled')
        elif choice == '2':
            print('Select your project type')
            print('1. Under supervising project')
            print('2. Other project')
            print('3. Cancel')
            choice = input('Input number(1-3): ')
            print()
            while choice != '3':
                if choice == '1':
                    for project_id in call_project_id(ID):
                        your_project = Project(project_id)
                        your_project.show()
                        your_project.show_proposal('faculty')
                        your_project.show_report('faculty')
                        print()
                elif choice == '2':
                    for _project in project.table:
                        if not isinproject(ID, _project):
                            project_id = copy.deepcopy(_project['ID'])
                            your_project = Project(project_id)
                            your_project.show()
                            print()
                print()
                print('Select your project type')
                print('1. Under supervising project')
                print('2. Other project')
                print('3. Cancel')
                choice = input('Input number(1-3): ')
                print()
        elif choice == '3':
            print('Select your project type to evaluate')
            print('1. Under supervising project')
            print('2. Other project')
            print('3. Cancel')
            choice = input('Input number(1-3): ')
            print()
            if choice == '1':
                k = 0
                available_id = []
                print('Project')
                print()
                for project_id in call_project_id(ID):
                    your_project = Project(project_id)
                    if your_project.status in ('Planned', 'Reported'):
                        k += 1
                        available_id.append(project_id)
                        print(f"{project_id:^8} | "
                              f"{your_project.title:<30} | "
                              f"Status: {your_project.status}")
                if k == 0:
                    print('You have no project to evaluate.')
                else:
                    print()
                    while True:
                        project_id = input('Insert ID of the project you want to evaluate: ')
                        if project_id in available_id:
                            break
                        print('Incorrect ID. Please try again')
                    if your_project.status == 'Planned':
                        your_project.show_proposal('faculty')
                    elif your_project.status == 'Reported':
                        your_project.show_report('faculty')
                    print('Please take your time to evaluate...')
                    print()
                    print('Evaluation result')
                    print('1. Pass')
                    print('2. Not pass')
                    print('3. Cancel')
                    choice = input('Input number(1-3): ')
                    print()
                    if choice == '1':
                        print('PASS')
                        if confirm():
                            if your_project.status == 'Planned':
                                your_project.status = 'In Progress'
                                request_auto_invalid(project_id)
                                # if proposal pass the pending request invalid.
                            elif your_project.status == 'Reported':
                                your_project.status = 'Advisor-approved'
                            your_project.update()
                            print('Evaluation confirmed')
                        else:
                            print('Evaluation canceled')
                    elif choice == '2':
                        print('NOT PASS')
                        if confirm():
                            if your_project.status == 'Planned':
                                your_project.status = 'Initiate'
                            elif your_project.status == 'Reported':
                                your_project.status = 'In progress'
                            your_project.update()
                            print('Evaluation confirmed')
                        else:
                            print('Evaluation canceled')
            elif choice == '2':
                k = 0
                available_id = []
                print('Project')
                print()
                for _project in project.filter(lambda x: x['status'] == 'Advisor-approved').table:
                    project_id = _project['ID']
                    if project_id not in call_project_id(ID):
                        your_project = Project(project_id)
                        k += 1
                        available_id.append(project_id)
                        print(f"{project_id:^8} | "
                              f"{your_project.title:<30} | "
                              f"Status: {your_project.status}")
                if k == 0:
                    print('There is no project to evaluate.')
                else:
                    print()
                    while True:
                        project_id = input('Insert ID of the project you want to evaluate: ')
                        if project_id in available_id:
                            break
                        print('Incorrect ID. Please try again')
                    your_project.show_report('faculty')
                    print('Please take your time to evaluate...')
                    print()
                    print('Evaluation result')
                    print('1. Pass')
                    print('2. Cancel')
                    choice = input('Input number(1-2): ')
                    print()
                    if choice == '1':
                        print('PASS')
                        if confirm():
                            your_project.status = 'Approved'
                            your_project.update()
                            print('Evaluation confirmed')
                        else:
                            print('Evaluation canceled')
        elif choice == '4':
            k = 0
            available_id = []
            for project_id in call_project_id(ID):
                your_project = Project(project_id)
                if your_project.status == 'Approve':
                    k += 1
                    available_id.append(project_id)
                    print(f"{project_id:^8} | "
                          f"{your_project.title:<30} | "
                          f"Status: {your_project.status}")
            if k == 0:
                print('You have no project to final approve.')
            else:
                print()
                while True:
                    project_id = input('Insert ID of the project you want to evaluate: ')
                    if project_id in available_id:
                        break
                    print('Incorrect ID. Please try again')
                your_project.show()
                your_project.show_proposal('faculty')
                your_project.show_report('faculty')
                print()
                print(f"{your_project.title} Project")
                print('1. Approve')
                print('2. Cancel')
                choice = input('Input number(1-2): ')
                print()
                if choice == '1':
                    print('APPROVE')
                    if confirm():
                        your_project.status = 'Completed'
                        your_project.update()
                        print('Approval confirmed')
                        print(f'{your_project.title} Project is completed.')
                    else:
                        print('Approval canceled')
        else:
            print('Incorrect input. Try again')
        print()
        print('Select your action')
        print('1. Requests')
        print('2. See project status')
        print('3. Evaluate project')
        print('4. Approve project')
        print('5. Exit')
        choice = input('Input number(1-5): ')
        print()


def admin():
    """ function for admin role """
    print('Select your action')
    print('1. See project data')
    print('2. Modify project data')
    print('3. See pending members data')
    print('4. Modify pending members requests data')
    print('5. See pending advisor requests data')
    print('6. Modify pending advisor requests data')
    print('7. Exit')
    choice = input('Input number(1-7): ')
    print()
    while choice != '7':
        if choice == '1':
            for _project in project.table:
                print(_project)
        elif choice == '2':
            table = copy.deepcopy(project)
            admin_modify(table)
        elif choice == '3':
            for request in member_pending_request.table:
                print(request)
        elif choice == '4':
            table = copy.deepcopy(member_pending_request)
            admin_modify(table)
        elif choice == '5':
            for request in advisor_pending_request.table:
                print(request)
        elif choice == '6':
            table = copy.deepcopy(advisor_pending_request)
            admin_modify(table)
        else:
            print('Incorrect input. Try again')
        print()
        print('Select your action')
        print('1. See project data')
        print('2. Modify project data')
        print('3. See pending members data')
        print('4. Modify pending members requests data')
        print('5. See pending advisor requests data')
        print('6. Modify pending advisor requests data')
        print('7. Exit')
        choice = input('Input number(1-7): ')
        print()


initializing()
val = login()
while val is None:
    print('Invalid username or password.')
    print()
    val = login()


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
elif role in ('faculty', 'advisor'):
    faculty()


exit()
