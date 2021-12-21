# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pydash import py_

from ..base import BaseModel
from .link import BaseCompendiumLink
from .descriptor import ExecutionDescriptor

from .type import is_draft, is_record


class CompendiumBase(BaseModel):
    """Base class for Compendium classes."""

    links_cls = BaseCompendiumLink
    descriptor_cls = ExecutionDescriptor

    def __init__(self, data=None, **kwargs):
        super(CompendiumBase, self).__init__(data or kwargs or {})

    @property
    def id(self):
        """Compendium id."""
        return self.get_field("id")

    @property
    def title(self):
        """Compendium title."""
        return self.get_field("metadata.title")

    @title.setter
    def title(self, title):
        py_.set_(self.data, "metadata.title", title)

    @property
    def description(self):
        """Compendium description."""
        return self.get_field("metadata.description")

    @description.setter
    def description(self, description):
        py_.set_(self.data, "metadata.description", description)

    @property
    def inputs(self):
        """Compendium input files."""
        _value_path = "metadata.execution.data.inputs"
        self._set_default_value(_value_path, [])

        return self.get_field(_value_path)

    @property
    def outputs(self):
        """Compendium output files."""
        _value_path = "metadata.execution.data.outputs"
        self._set_default_value(_value_path, [])

        return self.get_field(_value_path)

    @property
    def descriptor(self):
        """Compendium descriptor."""
        _value_path = "metadata.execution.environment.descriptor"
        self._set_default_value(_value_path, {})

        return self.descriptor_cls(data=self.get_field(_value_path))

    @descriptor.setter
    def descriptor(self, data):
        py_.set_(self.data, "metadata.execution.environment.descriptor", data)

    @property
    def metadata(self):
        """Compendium metadata."""
        return self.get_field("metadata.execution.environment.meta")

    @metadata.setter
    def metadata(self, metadata):
        py_.set_(self.data, "metadata.execution.environment.meta", metadata)

    @property
    def url(self):
        """Compendium URL."""
        return self.get_field("links.self")

    @property
    def links(self):
        """Compendium links."""
        return self.links_cls(py_.get(self.data, "links", None))

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
