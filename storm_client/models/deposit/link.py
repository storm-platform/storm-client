# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField, ObjectField


class DepositActionLink(BaseModel):
    """Deposit action link class."""

    start = DictField("start")
    """Link to start a deposit process."""

    cancel = DictField("cancel")
    """Link to cancel a deposit process."""


class DepositLink(BaseModel):
    """Deposit link class."""

    #
    # Data fields
    #

    self = LinkField("self", "Deposit")
    """Link to the Deposit itself in the service."""

    actions = ObjectField("actions", "DepositActionLink")
    """Link to the Deposit Actions itself in the service."""
