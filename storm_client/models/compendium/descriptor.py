# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from collections import UserDict


class ExecutionDescriptor(UserDict):
    def __init__(self, **kwargs):
        super(ExecutionDescriptor, self).__init__(kwargs or {})

    @property
    def name(self):
        return py_.get(self, "name")

    @property
    def uri(self):
        return py_.get(self, "uri")

    @property
    def version(self):
        return py_.get(self, "version")


__all__ = "ExecutionDescriptor"
