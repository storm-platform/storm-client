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
from ...field import DictField, ObjectField


class Deposit(BaseModel):
    """Deposit model.

    Deposit is a Storm WS job to send a project content
    (Metadata and pipeline data) to a external service
    like GEO Knowledge Hub and Zenodo.
    """

    #
    # Data fields
    #

    status = DictField("status")
    """Deposit status."""

    pipelines = DictField("pipelines")
    """Deposit defined pipelines."""

    service = DictField("service")
    """Deposit service."""

    project = DictField("project_id")
    """Deposit associated project."""

    customizations = DictField("customizations")
    """Project metadata customizations available in the Deposit service."""

    # Links
    links = ObjectField("links", "DepositLink")
    """Deposit links."""

    def __init__(self, data=None, **kwargs):
        super(Deposit, self).__init__(data or kwargs or {})

    def for_json(self):  # ``simplejson`` encoder method
        """Encode the object into a dict-like serializable object."""
        return py_.assign(
            py_.clone_deep(self.data),
            {
                "service": IDExtractor.extract(self.service),
                "pipelines": [IDExtractor.extract(i) for i in self.pipelines],
            },
        )


class DepositPluginService(BaseModel):
    """Deposit Plugin Service model.

    In the Deposit context on Storm WS, the deposit
    job can deposit data in many kinds of services.
    The Storm WS uses the Plugin Service concept to
    provide these different services. Each deposit
    target (e.g., GEO Knowledge Hub) is modeled as
    an individual service in this concept. The users
    can select these services and use them to send
    their data.

    This class represents the Deposit services available
    in the Storm WS.
    """

    #
    # Data fields
    #

    metadata = DictField("metadata")
    """Complete Deposit Plugin service metadata."""

    title = DictField("metadata.title")
    """Deposit Plugin service title (From metadata)."""

    description = DictField("metadata.description")
    """Deposit Plugin service description (From metadata)."""

    def __init__(self, data=None, **kwargs):
        super(DepositPluginService, self).__init__(data or kwargs or {})


class DepositList(UserList):
    """A collection of Deposits requests."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        data = py_.map(data, lambda obj: Deposit(obj))
        super(DepositList, self).__init__(data)


class DepositServiceList(UserList):
    """A collection of Deposits Services."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        super(DepositServiceList, self).__init__(
            py_.map(data, lambda obj: DepositPluginService(obj))
        )
