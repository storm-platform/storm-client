#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import os

import ast
import json

import asyncio

from pydash import py_

from collections import UserDict, UserList
from collections.abc import Sequence

from storm_client.network import HTTPXClient
from storm_client.models.base import BaseModel
from storm_client.object_factory import ObjectFactory


class NodeJSONEncoder(json.JSONEncoder):

    def _create_file_key(self, filename):
        if isinstance(filename, str):
            return {"key": os.path.join(filename)}
        return filename

    def default(self, o) -> dict:
        if isinstance(o, NodeBase):
            object_data = o.data

            # applying rules to convert files
            set_inputs = lambda data, prop: py_.set(data, prop,
                                                    py_.chain(data).get(prop).map(
                                                        self._create_file_key).value())

            set_inputs(object_data, "data.inputs")
            set_inputs(object_data, "data.outputs")

            return object_data

        raise TypeError("NodeJSONEncoder only encode `NodeBase` objects.")


#
# Node files
#
class NodeFileEntry(UserDict):
    def __init__(self, data=None):
        super(NodeFileEntry, self).__init__(data or {})

    @property
    def filename(self):
        return py_.get(self, "key")

    @property
    def size(self):
        return py_.get(self, "size")

    @property
    def checksum(self):
        return py_.get(self, "checksum")

    @property
    def mimetype(self):
        return py_.get(self, "mimetype")

    @property
    def content_url(self):
        return py_.get(self, "links.content", None)

    # ToDo: Implement the checksum validation
    def download(self, output_directory, validate_checksum=False):
        file_content_link = self.content_url

        if file_content_link:
            os.makedirs(output_directory, exist_ok=True)
            output_file = os.path.join(output_directory, self.filename)

            # download!
            asyncio.run(HTTPXClient.download(file_content_link, output_file))
            return output_file
        raise FileNotFoundError("File content is not available!")


class NodeFiles(UserList):

    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError('The `data` argument must be a valid sequence type.')

        data = [NodeFileEntry(file_entry) for file_entry in py_.get(data, [])]
        super(NodeFiles, self).__init__(data)


#
# Node links
#
class NodeLink(UserDict):

    def __init__(self, typename, data=None):
        super(NodeLink, self).__init__(data or {})

        self.typename = typename

    def __check_property(self, property_path):
        if not py_.has(self, property_path):
            raise AttributeError(f"{property_path} attribute not available for this object!")

    def __resolve_link(self, property_path, http_method="GET", typename=None):
        self.__check_property(property_path)

        # check if the type must be forced
        typename = typename if typename else self.typename

        # making the request
        response = asyncio.run(HTTPXClient.request(http_method, self[property_path])).json()

        if py_.has(response, "hits.hits"):  # for the `version` attribute
            return [
                ObjectFactory.resolve(typename, r) for r in py_.get(response, "hits.hits")
            ]

        if py_.has(response, "entries"):  # for the `files` attribute
            response = py_.get(response, "entries")

        return ObjectFactory.resolve(typename, response)

    @property
    def self(self):
        return self.__resolve_link("self")

    @property
    def latest(self):
        return self.__resolve_link("latest")

    @property
    def draft(self):
        # for the draft, `typename` always must be a `NodeDraft`
        return self.__resolve_link("latest", http_method="POST", typename="NodeDraft")

    @property
    def versions(self):
        return self.__resolve_link("versions")

    @property
    def files(self):
        return self.__resolve_link("files", http_method="GET", typename="NodeFiles")


class NodeDraftLink(NodeLink):
    def __init__(self, data=None):
        super(NodeDraftLink, self).__init__("NodeDraft", data or {})


class NodeRecordLink(NodeLink):
    def __init__(self, data=None):
        super(NodeRecordLink, self).__init__("NodeRecord", data or {})


#
# Node API
#
class NodeBase(BaseModel):
    links_cls = NodeLink
    serializer_cls = NodeJSONEncoder

    def __init__(self, data=None):
        super(NodeBase, self).__init__(data or {})

    @property
    def id(self):
        return py_.get(self, "id", None)

    @property
    def inputs(self):
        self._default_value("data.inputs", [])
        return py_.get(self, "data.inputs")

    @property
    def outputs(self):
        self._default_value("data.outputs", [])
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

    def to_json(self):
        return ast.literal_eval(json.dumps(self, cls=self.serializer_cls))


class NodeDraft(NodeBase):
    links_cls = NodeDraftLink


class NodeRecord(NodeBase):
    links_cls = NodeRecordLink


__all__ = (
    "NodeBase",
    "NodeDraft",
    "NodeRecord",

    "NodeFileEntry",
    "NodeFiles",

    "NodeDraftLink",
    "NodeRecordLink"
)
