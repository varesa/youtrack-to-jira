"""
Map Youtrack field values > Jira field values
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


issue_state_map = {
    "Submitted": "Submitted",
    "Open": "Submitted",
    "To be discussed": "Submitted",
    "Reopened": "Submitted",
    "Incomplete": "Submitted",
    "In Progress": "In Progress",
    "Fixed": "Billing",
    "Billed": "Closed",
    "Won't fix": "Closed",
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


# (Link name, Reverse)
issue_link_map = {
    "is required for": ("Blocks", False),
    "depends on": ("Blocks", True),
    "is duplicated by": ("Duplicate", False),
    "duplicates": ("Duplicate", True),
    "relates to": ("See also", False),
    "parent for": ("See also", False),
    "subtask of": ("See also", False)
}


def map_issue_link(link):
    if link in issue_link_map.keys():
        return issue_link_map[link]
    else:
        raise Exception("Unknown issue link {}, check mapping.py".format(link))
