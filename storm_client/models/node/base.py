#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import json
from json import JSONEncoder

from pydash import py_

from .link import NodeLink
from .files import map_file_entry
from .type import is_draft, is_record

from ..base import BaseModel


class NodeBase(BaseModel):
    links_cls = NodeLink
    serializer_cls = JSONEncoder

    def __init__(self, data=None):
        super(NodeBase, self).__init__(data or {})

    @property
    def id(self):
        return py_.get(self, "id", None)

    @property
    def inputs(self):
        self._default_value("data.inputs", [])

        map_file_entry(self.data, "data.inputs")
        return py_.get(self, "data.inputs")

    @property
    def outputs(self):
        self._default_value("data.outputs", [])

        map_file_entry(self.data, "data.outputs")
        return py_.get(self, "data.outputs")

    @property
    def environment(self):
        self._default_value("environment.key", None)
        return py_.get(self, "environment.key", None)

    @environment.setter
    def environment(self, data):
        py_.set_(self, "environment.key", str(data))

    @property
    def command(self):
        return py_.get(self, "command", None)

    @command.setter
    def command(self, data):
        py_.set_(self.data, "command", data)

    @property
    def command_checksum(self):
        return py_.get(self, "command_checksum", None)

    @command_checksum.setter
    def command_checksum(self, data):
        py_.set_(self.data, "command_checksum", data)

    @property
    def metadata(self):
        self._default_value("metadata", {"author": None, "description": None})
        return py_.get(self, "metadata", None)

    @metadata.setter
    def metadata(self, metadata):
        py_.set_(self.data, "metadata", metadata)

    @property
    def links(self):
        return self.links_cls(py_.get(self, "links", None))

    @property
    def is_draft(self):
        return is_draft(self.data)

    @property
    def is_record(self):
        return is_record(self.data)

    def to_json(self):
        return json.loads(json.dumps(self, cls=self.serializer_cls))


__all__ = (
    "NodeBase"
)
