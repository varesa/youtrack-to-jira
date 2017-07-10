import sys

from jira import Jira
from youtrack import Youtrack


username = input("Username: ")
password = input("Password: ")

youtrack = Youtrack().connect(username, password)
jira = Jira().connect(username, password)

project_key = "MBT"

projects = youtrack.get_projects(limit=project_key)

for project in projects:
    if project.id != project_key:
        continue
    if jira.does_project_exist(project.id):
        print("Project found in JIRA: " + project.id)
        jira.sync_project(project)
        stats = """
        Stats:
        Issues: {}
        Comments: {}
        Worklogs: {}
        Links: {}""".format(project.no_issues, project.no_comments, project.no_worklogs, project.no_links)
        sys.exit(0)

print("Project not found")


