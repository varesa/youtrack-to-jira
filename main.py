import sys

from config import Config, ConfigOption
from jira import Jira
from youtrack import Youtrack

config = Config((
    ConfigOption("USERNAME", "--username"),
    ConfigOption("PASSWORD", "--password"),
    ConfigOption("PROJECT", "--project"),
    ConfigOption("YOUTRACK_URL", "--youtrack"),
    ConfigOption("JIRA_URL", "--jira"),
)).get()

username = config["USERNAME"]
password = config["PASSWORD"]
project_key = config["PROJECT"]

youtrack = Youtrack(config["YOUTRACK_URL"]).connect(username, password)
jira = Jira(config["JIRA_URL"]).connect(username, password)

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


