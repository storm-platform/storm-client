# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import DictField


class ExecutionDescriptor(BaseModel):
    """Execution descriptor.

    An ``Execution Descriptor`` is the tool used to create
    the files that allow the reproduction of a research
    experiment.

    By default, an ``Execution Descriptor`` must define a metadata
    with the following properties:
        - uri;
        - name;
        - version.

    Also, other fields can be added.
    """

    #
    # Data fields
    #

    uri = DictField("uri")
    """Descriptor URI."""

    name = DictField("name")
    """Descriptor name."""

    version = DictField("version")
    """Descriptor version."""

    def __init__(self, **kwargs):
        super(ExecutionDescriptor, self).__init__(kwargs or {})
