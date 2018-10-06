import requests
import xml.etree.ElementTree as ET

from issue import Issue
from project import Project


def get_issue_fields(issue):
    d = {}
    for field in issue.findall('field'):
        if field.attrib['name'] == 'links':
            pass
        else:
            values = field.findall('value')
            if len(values) == 1:
                d[field.attrib['name']] = values[0].text
            elif len(values) > 1:
                raise Exception("Multiple values present for field {}".format(field.attrib['name']))
    return d


def get_issue_links(issue):
    for field in issue.findall('field'):
        if field.attrib['name'] == 'links':
            return [
                {'role': value.attrib['role'],
                 'type': value.attrib['type'],
                 'issue': value.text}
                for value in field.findall('value')
            ]


def get_issue_comments(issue):
    comments = []
    for comment in issue.findall('comment'):
        comments.append(comment.attrib)
    return comments


class Youtrack:

    url = ""
    headers = {}

    def __init__(self, url):
        self.url = url

    def connect(self, user, password):
        r = requests.post(self.url + "/rest/user/login", {'login': user, 'password': password})
        if r.status_code == 200:
            self.headers = {'Cookie': r.headers['Set-Cookie']}
            return self
        else:
            raise Exception("Error logging in: {}".format(r.status_code))

    def get_work(self, issue_id):
        r = requests.get(self.url + "/rest/issue/{}/timetracking/workitem/".format(issue_id), headers=self.headers)
        if r.status_code == 200:
            work = []
            root = ET.fromstring(r.text)
            for item in root.findall("workItem"):
                date = item.find('date').text
                duration = item.find('duration').text
                if item.find('description'):
                    description = item.find('description').text
                else:
                    description = ""
                author = item.find('author').text
                work.append({'date': date, 'duration': duration, 'author': author, 'description': description})
            return work
        elif r.status_code == 400:
            pass  # Work tracking not enabled
        else:
            raise Exception("Error getting work items for {} - {}".format(issue_id, r.status_code))

    def parse_issues(self, xml):
        issues = []
        root = ET.fromstring(xml)
        for issue in root.findall('issue'):
            print('.', end="")
            id       = issue.attrib['id']
            d        = get_issue_fields(issue)
            links    = get_issue_links(issue)
            comments = get_issue_comments(issue)
            work     = self.get_work(id)

            issue = Issue(id)\
                .from_dict(d)\
                .set_links(links)\
                .set_comments(comments)\
                .set_work(work)
            issues.append(issue)
            if str(issue) == "{}":
                raise Exception()
        return issues

    def parse_project(self, xml, limit=None):
        attribs = ET.fromstring(xml).attrib
        project = Project().from_dict(attribs)

        if limit and project.id != limit:
            return project

        r = requests.get(self.url + "/rest/issue/byproject/{}?max=10000".format(project.id), headers=self.headers)
        if r.status_code == 200:
            project.issues = self.parse_issues(r.text)
            return project
        else:
            raise Exception("Error getting project issues: {}".format(r.status_code))

    def parse_projects(self, xml, limit=None):
        projects = []
        projects_root = ET.fromstring(xml)
        for project in projects_root.findall('project'):
            print("Getting project", end="")
            url = project.attrib['url']
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                projects.append(self.parse_project(r.text, limit))
            else:
                raise Exception("Error getting project details: {}".format(r.status_code))
            print("")
        return projects

    def get_projects(self, limit=None):
        print("Getting project list")
        r = requests.get(self.url + "/rest/admin/project", headers=self.headers)
        if r.status_code == 200:
            return self.parse_projects(r.text, limit)
        else:
            raise Exception("Error getting projects: {}".format(r.status_code))
