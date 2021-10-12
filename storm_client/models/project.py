#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from pydash import py_

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


__all__ = (
    "Project"
)
