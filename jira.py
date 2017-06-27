import config


class Jira:

    url = ""

    def __init__(self):
        self.url = config.JIRA_URL

    def connect(self, user, password):
        return self
