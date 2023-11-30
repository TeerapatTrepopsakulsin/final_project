import database
import csv

project = database.Table('project')
project.insert('project.csv')

advisor_pending_request = database.Table('advisor_pending_request')
advisor_pending_request.insert('advisor_pending_request.csv')

member_pending_request = database.Table('member_pending_request')
member_pending_request.insert('member_pending_request.csv')

val = '1234567'
project1 = {'ID':'123456','title':'colourblind','lead':'pate','member1':'pete1','member2':'pete2','advisor':'run','status':'nothing'}
def see_project_status():
    print(project.table)

project.table.append(project1)

for i in project.table:
    if val ==
see_project_status()