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

project_key = "ALRK"

for project in projects:
    if project.id != project_key:
        continue
    if jira.does_project_exist(project.id):
        print("Project found in JIRA: " + project.id)
        jira.sync_project(project)
        print(project.__dict__)
        sys.exit(0)

print("Project not found")

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

