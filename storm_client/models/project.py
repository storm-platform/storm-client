# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from typing import Sequence
from collections import UserList

from storm_client.models.base import BaseModel


class Project(BaseModel):
    def __init__(self, data=None):
        super(Project, self).__init__(data or {})

    @property
    def id(self):
        return py_.get(self, "id", None)

    @property
    def title(self):
        return py_.get(self, "title", None)

    @property
    def name(self):
        return py_.get(self, "name", None)

    @property
    def is_public(self):
        return py_.get(self, "is_public", None)

    def to_json(self):
        return self.data


#
# Project Collection
#
class ProjectList(UserList):
    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError("The `data` argument must be a valid sequence type.")

        data = py_.map(data, lambda obj: Project(obj))
        super(ProjectList, self).__init__(data)


__all__ = ("Project", "ProjectList")
