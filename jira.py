import base64
import requests
import sys

import config
from jirameta import populate_meta
from mapping import map_issue_type


class Jira:

    url = ""
    headers = {}

    meta = {}

    def __init__(self):
        self.url = config.JIRA_URL

    def connect(self, user, password):
        self.headers = {'Authorization': "Basic " + base64.b64encode((user + ":" + password).encode()).decode()}
        r = requests.get(self.url + "/rest/auth/1/session", headers=self.headers)
        if r.status_code == 200:
            return self
        else:
            raise Exception("Error logging in: {}".format(r.status_code))

    def does_project_exist(self, id):
        r = requests.get(self.url + "/rest/api/2/project/" + id, headers=self.headers)
        if r.status_code == 200:
            return True
        else:
            return False

    def get_field_id(self, name):
        return self.meta['fields'][name]['id']

    def get_issuetype_id(self, project, name):
        return self.meta[project.id]['issuetypes'][name]['id']

    def create_issue(self, project, issue):
        print(issue.__dict__)
        data = {
            "fields": {
                "project": {
                    "key": project.id
                },
                "issuetype": {
                    "name": map_issue_type(issue.Type)
                },
                "summary": issue.summary,
                "description": issue.description

            }
        }
        r = requests.post(self.url + "/rest/api/2/issue", json=data, headers=self.headers)
        if r.status_code != 201:
            raise Exception("Error creating issue: {} - {}".format(r.status_code, r.text))

    def sync_project(self, project):
        populate_meta(self, project)
        #for issue in project.issues:
        issue = project.issues[0]
        self.create_issue(project, issue)
