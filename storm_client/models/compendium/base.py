# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pydash import py_

from ..base import BaseModel

from .type import is_draft, is_record
from ...field import DictField, ObjectField, LinkField


class CompendiumBase(BaseModel):
    """Base class for Compendium classes."""

    #
    # Data fields
    #

    # General informations
    versions = DictField("versions")
    """Versions dictionary."""

    revision_id = DictField("revision_id")
    """Revision ID."""

    is_published = DictField("is_published")
    """Flag indicating if the record is published."""

    parent = DictField("parent.id")
    """Parent ID."""

    # Metadata
    metadata = DictField("metadata")
    """Complete compendium metadata."""

    title = DictField("metadata.title")
    """Compendium title (From metadata)."""

    description = DictField("metadata.description")
    """Compendium description (From metadata)."""

    # Execution metadata
    inputs = DictField("metadata.execution.data.inputs", [])
    """Compendium execution input files."""

    outputs = DictField("metadata.execution.data.outputs", [])
    """Compendium execution output files."""

    environment = DictField("metadata.execution.environment", {})
    """Compendium execution environment complete metadata."""

    environment_metadata = DictField("metadata.execution.environment.meta")
    """Complete environment metadata."""

    environment_descriptor = ObjectField(
        "metadata.execution.environment.descriptor", "ExecutionDescriptor"
    )
    """Compendium execution environment descriptor metadata."""

    # Links
    links = LinkField("links", "BaseCompendiumLink")

    def __init__(self, data=None, **kwargs):
        super(CompendiumBase, self).__init__(data or kwargs or {})

    @property
    def is_draft(self):
        """Flag indicating if the compendium is a ``Draft``."""
        return is_draft(self.data)

    @property
    def is_record(self):
        """Flag indicating if the compendium is a ``Record``."""
        return is_record(self.data)

    def for_json(self):  # ``simplejson`` encoder method
        """Encode the object into a dict-like serializable object."""

        # special case: in the compendia, after encoding, we need
        # define the ``input`` and ``output`` in a special structure
        # required by the Storm WS.
        data = py_.clone_deep(self.data)  # cloning to avoid problems.
        (
            py_.chain(
                ["metadata.execution.data.inputs", "metadata.execution.data.outputs"]
            )
            .map(lambda path: (path, py_.get(data, path)))
            .map(
                lambda args: py_.set_(
                    data,
                    args[0],
                    py_.map(
                        args[1],
                        lambda file: {"key": os.path.join(file)}
                        if type(file) != dict
                        else file,
                    ),
                )
            )
            .value()
        )

        return data
