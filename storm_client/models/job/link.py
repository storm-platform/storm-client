# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField, ObjectField


class JobActionLink(BaseModel):
    """Job action link class."""

    start = DictField("start")
    """Link to start a Job process."""

    cancel = DictField("cancel")
    """Link to cancel a Job process."""


class JobLink(BaseModel):
    """Job link class."""

    #
    # Data fields
    #

    self = LinkField("self", "Job")
    """Link to the Deposit itself in the service."""

    actions = ObjectField("actions", "JobActionLink")
    """Link to the Job Actions itself in the service."""
