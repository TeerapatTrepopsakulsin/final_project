# About how it's working

* Student
    1. Requests
       * show pending requests to become members of already created projects
       * choose to accept or deny
       * role become 'member' and become member of the project if accepted the request
    2. Create a project
       * role become 'leader'
    

* Leader
    1. See project status
        * show project information
    2. Modify project information
    3. Responded requests
        * show how request responded (accepted or denied)
    4. Send out members requests
        * add request into Member_pending_request table
        * cannot send out if there is pending request remain
    5. Send out advisor requests
        * add request into Advisor_pending_request table
        * cannot send out if there is pending request remain


* Member
    1. See project status
    2. Modify project information
    3. Responded requests
       * show how request by the leader responded (accepted or denied)


* Faculty
    1. Requests
       * show pending requests to become advisor of already created projects
       * choose to accept or deny
       * role become 'advisor' and become advisor of the project if accepted the request
    2. See all project status
       * show all project information 
    3. Evaluate projects
       * in Proposal.md file
      
 
* Advisor
    1. Requests
       * show pending requests to become advisor of already created projects
       * choose to accept or deny
       * role become 'advisor' and become advisor of the project if accepted the request
    2. See all project status
       * show all project information 
    3. Evaluate projects
       * in Proposal.md file


* Admin
    1. See all project status
        * show all project information
    2. Modify  project information
    3. See all advisor request status
          * show all advisor request information
    4. Modify advisor request information
    5. See all member request status
        * show all member request information
    6. Modify member request information


### Note
- Project status:
  * Not started 
    - no advisor supervised
  * Initiate            
    - advisor has supervised
  * Planned
    - lead sent the proposal to advisor
  * In progress 
    - advisor approved proposal
  * Reported
    - lead sent the report to advisor
  * Advisor-approved 
    - advisor approved report
  * Approved 
    - another faculty approved report
  * Completed 
    - advisor approved project
