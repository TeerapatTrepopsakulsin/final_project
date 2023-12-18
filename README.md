# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

## Files
* database.py
  * class
    * Database
      * a data storage of every table
    * Table
      * contains specific data
      * link with each specific csv files
      * can update data into csv files
* project_manage.py
  * class
    * Project
      * is a class of a project
      * can use for the interaction with many action of vary roles
      * can update itself into Project.csv file
* minor_function.py
  * side notes, unused
* persons.csv
  * contains ID, name and main role
  * main role
    * student
    * faculty
    * admin
  * cannot be changed
* login.csv
  * contains ID, username, password and role
  * role
    * student
    * member
    * lead
    * faculty
    * advisor
    * admin
* project.csv
  * contains project ID, title, member ID (including lead and advisor), proposal and report
* member_pending_request.csv
  * contains project ID, member ID, response status and response date
* advisor_pending_request.csv
  * contains project ID, advisor ID, response status and response date
* Checklist.md
  * a checklist of main action in each role
* Proposal.md
  * an outline of project evaluation step in lead, faculty and advisor role
* TODO.md
  * an outline of main action in each role (project evaluation excluded)
* README.md


## How to compile and run
  * the system bring up the updated data from the csv files
  * login with different username will lead to different role according to the role in login.csv
  * choice pops up according to the different role
  * if user choose an exit choice means all actions are done 
(or possibly some specific action which require logging out automatically)
  * all data that have changed from the action will be returned back to csv files


## Role and Action
|  Roles   | Action                               |                         Method                         |      Class      | Completion percentage | 
|:--------:|:-------------------------------------|:------------------------------------------------------:|:---------------:|:---------------------:|
| student  | Check requests                       |                          show                          |     Project     |         100%          |
| student  | Accept / deny requests               |           update / set_row, set_row_advanced           | Project / Table |         100%          |
| student  | Create project                       |                        set_row                         |      Table      |         100%          |
|   lead   | See project status                   |            show, show_proposal, show_report            |     Project     |         100%          |
|   lead   | Modify project information           |       update, modify, show_proposal, show_report       | Project / Table |         100%          |
|   lead   | Check requests history               |                      show_request                      |     Project     |         100%          |
|   lead   | Send out members requests            |                  send_member_request                   |     Project     |         100%          |
|   lead   | Send out advisor requests            |                  send_advisor_request                  |     Project     |         100%          |
|   lead   | Cancel members requests              |                 cancel_member_request                  |     Project     |         100%          |
|   lead   | Cancel advisor requests              |                 cancel_advisor_request                 |     Project     |         100%          |
|   lead   | Request for project evaluation       | update, evaluation_request, show_proposal, show_report | Project / Table |         100%          |
|  member  | See project status                   |            show, show_proposal, show_report            |     Project     |         100%          |
|  member  | Modify project information           |       update, modify, show_proposal, show_report       | Project / Table |         100%          |
|  member  | Check requests history               |                      show_request                      |     Project     |         100%          |
| faculty  | Check requests                       |                          show                          |     Project     |         100%          |
| faculty  | Accept / deny requests               |           update / set_row, set_row_advanced           | Project / Table |         100%          |
| faculty  | See project status                   |                          show                          |     Project     |         100%          |
| faculty  | Evaluate project                     |                  update, show_report                   | Project / Table |         100%          |
| advisor  | See under-supervising project status |            show, show_proposal, show_report            |     Project     |         100%          |
| advisor  | Evaluate under-supervising project   |           update, show_proposal, show_report           | Project / Table |         100%          |
| advisor  | Approve project                      |        update, show, show_proposal, show_report        | Project / Table |         100%          |
|  admin   | See tables data                      |                           -                            |      Table      |          85%          |
|  admin   | Modify tables data                   |                 admin_modify, set_row                  |      Table      |          75%          |


## Missing features and bugs
  * admin role interface lacking
  * admin modifying system can cause error if there is duplicated 'ID'
  * I've put some function fragment in to a class in the last commit(but barely modify anything)