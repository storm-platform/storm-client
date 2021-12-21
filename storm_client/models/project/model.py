# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from collections import UserList
from storm_client.models.base import BaseModel


class Project(BaseModel):
    """Research Project model.

    A ``Research Project`` is a unity to centralize
    and organize all elements of an research, including
    ``people``, ``data``, ``software``.
    """

    def __init__(self, data=None, **kwargs):
        super(Project, self).__init__(data or kwargs or {})

    @property
    def id(self):
        """Project id."""
        return self.get_field("id")

    @property
    def title(self):
        """Project title."""
        return self.get_field("metadata.title")

    @property
    def description(self):
        """Project description."""
        return self.get_field("metadata.description")

    @property
    def metadata(self):
        """Project complete metadata."""
        return self.get_field("metadata")

    @property
    def url(self):
        """Project URL."""
        return self.get_field("links.self")


class ProjectList(UserList):
    """A collection of Research projects."""

    def __init__(self, data=None):
        # fixme: this is in the wrong place.
        if py_.has(data, "hits.hits"):  # elasticsearch specific result format
            data = py_.get(data, "hits.hits")

        if not isinstance(data, (list, tuple)):
            raise ValueError(
                "The `data` argument must be a valid ``list`` or ``tuple`` type."
            )

        data = py_.map(data, lambda obj: Project(obj))
        super(ProjectList, self).__init__(data)
