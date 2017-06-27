
class Project:
    issues = []

    def __init__(self):
        pass

    def __str__(self):
        return str(self.__dict__)

    def from_dict(self, d):
        for key in d.keys():
            self.__dict__[key] = d[key]
        return self
