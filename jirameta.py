import requests


def meta_issuetypes(jira, project):
    r = requests.get(jira.url + "/rest/api/2/issue/createmeta?projectKeys=" + project.id, headers=jira.headers)
    if r.status_code == 200:
        data = r.json()
        if data['projects'][0]['key'] != project.id:
            raise Exception("Didn't get the issue creation metadata for the project we asked for: {}/{}"
                            .format(data['projects'][0]['key'], project.id))
        for issuetype in data['projects'][0]['issuetypes']:
            jira.meta[project.id]["issuetypes"][issuetype['name']] = issuetype
    else:
        raise Exception("Error getting issue creation metadata: {}".format(r.status_code))


def meta_fields(jira):
    if "fields" in jira.meta.keys():
        return
    else:
        jira.meta['fields'] = {}
    r = requests.get(jira.url + "/rest/api/2/field", headers=jira.headers)
    if r.status_code == 200:
        fields = r.json()
        for field in fields:
            jira.meta["fields"][field['name']] = field
    else:
        raise Exception("Error getting list of fields: {}".format(r.status_code))


def populate_meta(jira, project):
    meta_fields(jira)

    if project.id not in jira.meta.keys():
        jira.meta[project.id] = {"issuetypes": {}}
        meta_issuetypes(jira, project)
