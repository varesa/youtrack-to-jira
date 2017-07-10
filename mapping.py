"""
Map Youtrack field values > Jira field values
"""

"""
Issue type
Bug			        -> Bug
Cosmetics		    -> Improvement
Exception		    -> Bug
Feature			    -> New Feature
Task			    -> Task
Usability Problem	-> Bug
Performance Problem	-> Bug
Epic			    -> Epic
"""

issue_type_map = {
    "Bug": "Bug",
    "Cosmetics": "Improvement",
    "Feature": "New Feature",
    "Task": "Task",
    "Usability Problem": "Bug",
    "Performance Problem": "Bug",
    "Epic": "Epic"
}


def map_issue_type(type):
    if type in issue_type_map.keys():
        return issue_type_map[type]
    else:
        raise Exception("Unknown issue type {}, check mapping.py".format(type))


"""
Priority
low			    -> Low
high			-> High
Minor			-> Low
Normal			-> Medium
Major			-> High
Critical		-> Highest
Show-stopper	-> Highest
"""

issue_priority_map = {
    "low": "Low",
    "Minor": "Low",
    "Normal": "Medium",
    "high": "High",
    "Major": "High",
    "Critical": "Highest",
    "Show-stopper": "Highest"

}


def map_issue_priority(priority):
    if priority in issue_priority_map.keys():
        return issue_priority_map[priority]
    else:
        raise Exception("Unknown issue priority {}, check mapping.py".format(priority))


"""
State
Submitted		-> Submitted
Open			-> Submitted
To be discussed	-> Submitted
Reopened		-> Submitted
Incomplete		-> Submitted
In Progress		-> In Progress
Billed			-> Billed
Fixed			-> Fixed
Won't Fix		-> Closed
Obsolete		-> Closed
Verified		-> Closed
Can't Reproduce	-> Closed
Duplicate		-> Closed
"""

issue_state_map = {
    "Submitted": "Submitted",
    "Open": "Submitted",
    "To be discussed": "Submitted",
    "Reopened": "Submitted",
    "Incomplete": "Submitted",
    "In Progress": "In Progress",
    "Fixed": "Fixed",
    "Won't Fix": "Closed",
    "Obsolete": "Closed",
    "Verified": "Closed",
    "Can't Reproduce": "Closed",
    "Duplicate": "Closed"
}


def map_issue_state(state):
    if state in issue_state_map.keys():
        return issue_state_map[state]
    else:
        raise Exception("Unknown issue state {}, check mapping.py".format(state))
