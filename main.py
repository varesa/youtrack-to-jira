from jira import Jira
from youtrack import Youtrack


username = input("Username: ")
password = input("Password: ")

youtrack = Youtrack().connect(username, password)
jira = Jira().connect(username, password)

projects = youtrack.get_projects()
print(projects)


