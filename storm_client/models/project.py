
from collections import UserDict


class Project(UserDict):

    def __init__(self, data=None):
        super(Project, self).__init__(data or {})


__all__ = (
    "Project"
)
