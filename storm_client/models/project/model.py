# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from collections import UserList

from ..base import BaseModel
from ...field import DictField


class Project(BaseModel):
    """Research Project model.

    A ``Research Project`` is a unity to centralize
    and organize all elements of an research, including
    ``people``, ``data``, ``software``.
    """

    #
    # Data fields
    #

    # General informations
    is_finished = DictField("is_finished")
    """Flag indicating if the workflow is finished."""

    revision_id = DictField("revision_id")
    """Revision ID."""

    # Metadata
    metadata = DictField("metadata")
    """Complete Project metadata."""

    title = DictField("metadata.title")
    """Project title (From metadata)."""

    description = DictField("metadata.description")
    """Project description (From metadata)."""

    def __init__(self, data=None, **kwargs):
        super(Project, self).__init__(data or kwargs or {})


class ProjectList(UserList):
    """A collection of Research projects."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        super(ProjectList, self).__init__(py_.map(data, lambda obj: Project(obj)))
