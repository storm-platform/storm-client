# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_
from collections import UserList

from ..base import BaseModel
from ..extractor import IDExtractor
from ...field import DictField


class Job(BaseModel):
    """Job model.

    Once a pipeline is finished, it can be
    rerun for validation and reproduction of
    the results. To perform these operations,
    in Storm WS, Jobs are created. A Job
    represents an execution (New or Finished).

    Once created, it is possible to define the
    service where the job will be executed and
    then perform its execution.
    """

    #
    # Data fields
    #

    status = DictField("status")
    """Deposit status."""

    service = DictField("service")
    """Deposit service."""

    project_id = DictField("project_id")
    """Deposit associated project."""

    pipeline_id = DictField("pipeline_id")
    """Deposit defined pipelines."""

    def __init__(self, data=None, **kwargs):
        super(Job, self).__init__(data or kwargs or {})

    def for_json(self):  # ``simplejson`` encoder method
        """Encode the object into a dict-like serializable object."""

        return py_.assign(
            py_.clone_deep(self.data),
            {
                "service": IDExtractor.extract(self.service),
                "pipeline_id": IDExtractor.extract(self.pipeline_id),
                "project_id": IDExtractor.extract(self.project_id),
            },
        )


class JobPluginService(BaseModel):
    """Job Plugin Service model.

    A job can run on different services. In
    Storm WS, these services are represented
    as Plugin services.
    """

    #
    # Data fields
    #

    metadata = DictField("metadata")
    """Complete Job Plugin service metadata."""

    title = DictField("metadata.title")
    """Job Plugin service title (From metadata)."""

    description = DictField("metadata.description")
    """Job Plugin service description (From metadata)."""

    def __init__(self, data=None, **kwargs):
        super(JobPluginService, self).__init__(data or kwargs or {})


class JobList(UserList):
    """A collection of Deposits requests."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        data = py_.map(data, lambda obj: Job(obj))
        super(JobList, self).__init__(data)


class JobServiceList(UserList):
    """A collection of Job Services."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        super(JobServiceList, self).__init__(
            py_.map(data, lambda obj: JobPluginService(obj))
        )
