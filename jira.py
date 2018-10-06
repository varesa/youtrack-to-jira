import base64
import datetime
import requests

from jirameta import populate_meta
from mapping import map_issue_type, map_issue_priority, map_issue_state, map_issue_link


class Jira:

    url = ""
    headers = {}

    meta = {}

    issue_map = {}

    def __init__(self, url):
        self.url = url

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

    def transition_issue(self, project, issue):
        r = requests.get(self.url + "/rest/api/2/issue/{}/transitions?expand=transitions.fields".format(issue.jira_id),
                         headers=self.headers)
        if r.status_code != 200:
            raise Exception("Error getting issue transitions: {} - {}".format(r.status_code, r.text))
        transitions = r.json()['transitions']

        new_state = map_issue_state(issue.State)
        transition_id = None
        for transition in transitions:
            if transition['to']['name'] == new_state:
                transition_id = transition['id']
        if transition_id is None:
            raise Exception("Error: No transition found to state {} (mapped from {})".format(new_state, issue.State))

        r = requests.post(self.url + "/rest/api/2/issue/{}/transitions".format(issue.jira_id),
                          json={"transition": {"id": transition_id}},
                          headers=self.headers)

        if r.status_code != 204:
            raise Exception("Error changing issue state: {} - {}".format(r.status_code, r.text))

    def create_comments(self, project, issue):
        for comment in issue.comments:
            text = comment['authorFullName'] + " (Youtrack) commented on " \
                   + datetime.datetime.fromtimestamp(int(comment['created'][:-3])-10800).isoformat() + " (GMT):\n\n" \
                   + comment['text']
            r = requests.post(self.url + "/rest/api/2/issue/{}/comment".format(issue.jira_id),
                              json={'body': text},
                              headers=self.headers)
            if r.status_code != 201:
                raise Exception("Error creating comment: {} - {}".format(r.status_code, r.text))

            project.no_comments += 1

    def create_worklog(self, project, issue):
        for log in issue.work:
            data = {
                "started": datetime.datetime.fromtimestamp(int(log['date'][:-3])).isoformat()+".000+0300",
                "timeSpentSeconds": int(log['duration'])*60,
                "comment": log['description']
            }
            r = requests.post(self.url + "/rest/api/2/issue/{}/worklog".format(issue.jira_id),
                              json=data,
                              headers=self.headers)
            if r.status_code != 201:
                raise Exception("Error creating worklog: {} - {}".format(r.status_code, r.text))

            project.no_worklogs += 1

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
                "description": issue.description if 'description' in issue.__dict__.keys() else "",

                "priority": {
                    "name": map_issue_priority(issue.Priority)
                },

                self.get_field_id("Youtrack ID"): issue.id,
                self.get_field_id("Youtrack State"): {
                    "value": issue.State
                },

                self.get_field_id("Youtrack Created"):
                    datetime.datetime.fromtimestamp(int(issue.created[:-3])).isoformat()+".000+0300",
                self.get_field_id("Youtrack Updated"):
                    datetime.datetime.fromtimestamp(int(issue.updated[:-3])).isoformat()+".000+0300",

                self.get_field_id("Billed"): str(int(issue.Billedtime)/60) + " h"
                if 'Billedtime' in issue.__dict__.keys() else ""
            }
        }
        if 'resolved' in issue.__dict__.keys():
            data['fields'][self.get_field_id("Youtrack Resolved")] = datetime.datetime.fromtimestamp(
                int(issue.resolved[:-3])).isoformat() + ".000+0300"
        r = requests.post(self.url + "/rest/api/2/issue", json=data, headers=self.headers)
        if r.status_code != 201:
            raise Exception("Error creating issue: {} - {}".format(r.status_code, r.text))
        issue.jira_id = r.json()['id']
        self.issue_map[issue.id] = issue.jira_id

        project.no_issues += 1

        self.transition_issue(project, issue)
        self.create_comments(project, issue)
        self.create_worklog(project, issue)

    def create_links(self, project):
        links = {}
        for issue in project.issues:
            if issue.links is None:
                continue
            for link in issue.links:
                if (link['issue'], issue.id) not in links.keys():
                    links[(issue.id, link['issue'])] = {**link, 'from': issue.id}
        for pair in links:
            link = links[pair]
            if map_issue_link(link['role'])[1]:
                inwards = link['issue']
                outwards = link['from']
            else:
                inwards = link['from']
                outwards = link['issue']
            data = {
                "type": {"name": map_issue_link(link['role'])[0]},
                "inwardIssue": {"id": self.issue_map[inwards]},
                "outwardIssue": {"id": self.issue_map[outwards]}
            }
            r = requests.post(self.url + "/rest/api/2/issueLink", json=data, headers=self.headers)
            if r.status_code != 201:
                raise Exception("Error creating issue link: {} - {}".format(r.status_code, r.text))
            project.no_links += 1

    def sync_project(self, project):
        populate_meta(self, project)

        for issue in project.issues:
            self.create_issue(project, issue)
        self.create_links(project)
