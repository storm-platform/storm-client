# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField, ObjectField


class WorkflowActionLink(BaseModel):
    """Workflow action link class."""

    add_compendium = DictField("add-compendium")
    """Link to add a compendium in the workflow."""

    delete_compendium = DictField("delete-compendium")
    """Link to delete a compendium in the workflow."""


class WorkflowLink(BaseModel):
    """Workflow link class."""

    #
    # Data fields
    #

    self = LinkField("self", "Workflow")
    """Link to the Pipeline itself in the service."""

    actions = ObjectField("actions", "WorkflowActionLink")
    """Link to the Pipeline Actions in the service."""
