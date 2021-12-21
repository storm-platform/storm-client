# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel


class ExecutionDescriptor(BaseModel):
    """Execution descriptor.

    An ``Execution Descriptor`` is the tool used to create
    the files that allow the reproduction of a research
    experiment.

    By default, an ``Execution Descriptor`` must define a metadata
    with the following properties:
        - name;
        - uri;
        - version.

    Also, other fields can be added.
    """

    def __init__(self, **kwargs):
        super(ExecutionDescriptor, self).__init__(kwargs or {})

    @property
    def name(self):
        """Execution descriptor name."""
        return self.get_field("name")

    @property
    def uri(self):
        """Execution descriptor URI."""
        return self.get_field("uri")

    @property
    def version(self):
        """Execution descriptor version."""
        return self.get_field("version")

    def for_json(self):
        return self.data
