# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField, ObjectField


class ExecutionJobActionLink(BaseModel):
    """Job action link class."""

    start = DictField("start")
    """Link to start a Job process."""

    cancel = DictField("cancel")
    """Link to cancel a Job process."""


class ExecutionJobLink(BaseModel):
    """Job link class."""

    #
    # Data fields
    #

    self = LinkField("self", "ExecutionJob")
    """Link to the Deposit itself in the service."""

    actions = ObjectField("actions", "ExecutionJobActionLink")
    """Link to the Execution Job Actions itself in the service."""
