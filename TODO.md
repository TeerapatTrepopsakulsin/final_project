create function for every role

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