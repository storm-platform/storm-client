# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField, ObjectField


class PipelineActionLink(BaseModel):
    """Pipeline action link class."""

    add_compendium = DictField("add-compendium")
    """Link to add a compendium in the pipeline."""

    delete_compendium = DictField("delete-compendium")
    """Link to delete a compendium in the pipeline."""


class PipelineLink(BaseModel):
    """Pipeline link class."""

    #
    # Data fields
    #

    self = LinkField("self", "Pipeline")
    """Link to the Pipeline itself in the service."""

    actions = ObjectField("actions", "PipelineActionLink")
    """Link to the Pipeline itself in the service."""
