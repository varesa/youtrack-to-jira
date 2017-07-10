
class Project:
    issues = []

    no_issues = 0
    no_comments = 0
    no_links = 0
    no_worklogs = 0

    def __init__(self):
        pass

    def __str__(self):
        return str(self.__dict__)

    def from_dict(self, d):
        for key in d.keys():
            self.__dict__[key.replace(' ', '')] = d[key]
        return self
