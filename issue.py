

class Issue:

    id = ""

    comments = []
    links = []
    work = []

    def __init__(self, id=""):
        self.id = id

    def __str__(self):
        return str(self.__dict__)

    def from_dict(self, d):
        for key in d.keys():
            self.__dict__[key] = d[key]
        return self

    def set_links(self, links):
        self.links = links
        return self

    def set_comments(self, comments):
        self.comments = comments
        return self

    def set_work(self, work):
        self.work = work
        return self
