import sys

from jira import Jira
from youtrack import Youtrack


username = input("Username: ")
password = input("Password: ")

youtrack = Youtrack().connect(username, password)
jira = Jira().connect(username, password)

projects = youtrack.get_projects()

states = {}
types = {}
priorities = {}
resolutions = {}


def increment(d, key):
    if key not in d.keys():
        d[key] = 1
    else:
        d[key] += 1

for project in projects:
    if jira.does_project_exist(project.id):
        print("Project found in JIRA: " + project.id)
        if project.id != "ALRK":
            continue
        jira.sync_project(project)

    else:
        print("Project not found in JIRA: " + project.id)

"""if True:
    for project in projects:
        for issue in project.issues:
            try:
                increment(states, issue.State)
                increment(types, issue.Type)
                increment(priorities, issue.Priority)
                if "Resolution" in issue.__dict__:
                    increment(resolutions, issue.Resolution)

                else:
                    increment(resolutions, "Not set")
            except:
                print(issue)

print("Things:")
print(states)
print(types)
print(priorities)
print(resolutions)"""

