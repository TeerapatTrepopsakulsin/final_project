import copy
import random
import sys
import database
import csv
from time import time,strftime,localtime

project = database.Table('project')
project.insert('project.csv')

advisor_pending_request = database.Table('advisor_pending_request')
advisor_pending_request.insert('advisor_pending_request.csv')

member_pending_request = database.Table('member_pending_request')
member_pending_request.insert('member_pending_request.csv')

persons = database.Table('persons')
persons.insert('persons.csv')

login_table = database.Table('login')
login_table.insert('login.csv')


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


def set_row(table, id_value, update_attribute, update_value):
    for i in table:
        if i['ID'] == id_value:
            i[update_attribute] = update_value


def get_row(table, id_value, attribute):
    for i in table:
        if i['ID'] == id_value:
            return i[attribute]




val = '1234567'
project1 = {'ID':'1234567','title':'colourblind','lead':'1235567','member1':'1234568','member2':None,'advisor':'1234888','status':'nothing'}
pending_member = {'ID':'1234567','member':'2235567','response':None,'response_date':None}
pending_advisor = {'ID':'1234567','advisor':'2235567','response':'1235567','response_date':'1234568'}

#project.table.append(project1)

for project in project.table:
    if val == project['member1'] or val == project['member2'] or val == project['lead'] or val == project['advisor']:
        print(project)


def create_project_id():
    exist_id = ['1111111']
    print(exist_id)
    selected_id = random.sample([str(i) for i in range(1000000,9999999) if str(i) not in exist_id])
    return selected_id

test = '1234567,0000000,,'
print(strftime("%d/%b/%Y", localtime(time())))

print(project)
class Project:
    def __init__(self, ID):
        self.ID = ID
        self.title = get_row(project.table, ID, 'title')
        self.lead = get_row(project.table, ID, 'lead')
        self.member1 = get_row(project.table, ID, 'member1')
        self.member2 = get_row(project.table, ID, 'member2')
        self.advisor = get_row(project.table, ID, 'advisor')
        self.status = get_row(project.table, ID, 'status')

    def show(self):
        return (f'Project title: {self.title}'
                f'Lead: {identify(self.lead)}'
                f'Member: {identify(self.member1)}'
                f'Member: {identify(self.member2)}'
                f'Advisor: {identify(self.advisor)}'
                f'Project status: {self.status}')


print(Project('1234567'))
