from sys import maxsize


class Project:

    def __init__(self, name=None, description=None, project_id=None):
        self.name = name
        self.description = description
        self.project_id = project_id

    def __repr__(self):
        return "%s:%s;%s" % (self.project_id, self.name, self.description)

    def __eq__(self, other):
        return self.project_id is None or other.project_id is None or self.project_id == other.project_id and self.name == other.name

    def project_id_or_max(self):
        if self.project_id:
            return int(self.project_id)
        else:
            return maxsize
