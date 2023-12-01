import database
import  random
import csv

project = database.Table('project')
project.insert('project.csv')

advisor_pending_request = database.Table('advisor_pending_request')
advisor_pending_request.insert('advisor_pending_request.csv')

member_pending_request = database.Table('member_pending_request')
member_pending_request.insert('member_pending_request.csv')

def int_autocorrect(num, a):
    if isinstance(num, int):
        return num
    return a


def set_row(table, id_value, update_attribute, update_value):
    for i in table:
        if i['ID'] == id_value:
            i[update_attribute] = update_value

val = '1234567'
project1 = {'ID':'1234567','title':'colourblind','lead':'1235567','member1':'1234568','member2':None,'advisor':'1234888','status':'nothing'}
pending_member = {'ID':'1234567','member':'2235567','response':'1235567','response_date':'1234568'}

#project.table.append(project1)

for project in project.table:
    if val == project['member1'] or val == project['member2'] or val == project['lead'] or val == project['advisor']:
        print(project)


def create_project_id():
    exist_id = ['1111111']
    print(exist_id)
    selected_id = random.sample([str(i) for i in range(1000000,9999999) if str(i) not in exist_id])
    return selected_id
