# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
from json import JSONEncoder

from pydash import py_

from .link import CompendiumLink
from .files import map_file_entry
from .type import is_draft, is_record

from .descriptor import ExecutionDescriptor

from ..base import BaseModel


class CompendiumBase(BaseModel):
    links_cls = CompendiumLink
    serializer_cls = JSONEncoder
    descriptor_cls = ExecutionDescriptor

    def __init__(self, data=None):
        super(CompendiumBase, self).__init__(data or {})

    @property
    def id(self):
        return py_.get(self.data, "id", None)

    @property
    def title(self):
        return py_.get(self.data, "metadata.title", None)

    @title.setter
    def title(self, title):
        py_.set_(self.data, "metadata.title", title)

    @property
    def description(self):
        return py_.get(self.data, "metadata.description", None)

    @description.setter
    def description(self, description):
        py_.set_(self.data, "metadata.description", description)

    @property
    def inputs(self):
        _value_path = "metadata.execution.data.inputs"
        self._default_value(_value_path, [])

        map_file_entry(self.data, _value_path)
        return py_.get(self.data, _value_path)

    @property
    def outputs(self):
        _value_path = "metadata.execution.data.outputs"
        self._default_value(_value_path, [])

        map_file_entry(self.data, _value_path)
        return py_.get(self.data, _value_path)

    @property
    def descriptor(self):
        _value_path = "metadata.execution.environment.descriptor"
        self._default_value(_value_path, {})

        return self.descriptor_cls(data=py_.get(self.data, _value_path, None))

    @descriptor.setter
    def descriptor(self, data):
        _value_path = "metadata.execution.environment.descriptor"
        py_.set_(self.data, _value_path, data)

    @property
    def metadata(self):
        _value_path = "metadata.execution.environment.meta"
        return py_.get(self.data, _value_path, None)

    @metadata.setter
    def metadata(self, metadata):
        _value_path = "metadata.execution.environment.meta"
        py_.set_(self.data, _value_path, metadata)

    @property
    def errors(self):
        return py_.get(self.data, "errors", [])

    @property
    def links(self):
        return self.links_cls(py_.get(self.data, "links", None))

    @property
    def is_draft(self):
        return is_draft(self.data)

    @property
    def is_record(self):
        return is_record(self.data)

    def to_json(self):
        return json.loads(json.dumps(self, cls=self.serializer_cls))


__all__ = "CompendiumBase"
