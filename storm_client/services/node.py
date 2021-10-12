#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from typing import Union

import posixpath

import asyncio
from pydash import py_
from cachetools import cached, LRUCache

from storm_client.network import HTTPXClient
from storm_client.models.node.base import NodeBase
from storm_client.services.base import BaseService
from storm_client.object_factory import ObjectFactory


class NodeService(BaseService):

    def __init__(self, url: str, access_token: str, project_id: int, as_draft=False) -> None:
        base_path = posixpath.join("graph", str(project_id), "node")
        super(NodeService, self).__init__(url, base_path, access_token)

        self._as_draft = as_draft
        self._project_id = project_id

        # defining the node type
        self._node_type = "NodeRecord"
        self._complement_url = ""

        if as_draft:
            self._node_type = "NodeDraft"
            self._complement_url = "draft"

    @property
    def is_draft_service(self):
        return self._as_draft

    @cached(cache=LRUCache(maxsize=128))
    def search(self, **kwargs):
        operation_result = self._create_request("GET", self.url, **kwargs)

        return [
            ObjectFactory.resolve(self._node_type, response) for response in
            py_.get(operation_result.json(), "hits.hits", {})
        ]

    def resolve(self, node_id: str, **kwargs) -> Union[NodeBase, None]:
        node_id_url = self._build_url([node_id, self._complement_url])
        operation_result = self._create_request("GET", node_id_url, **kwargs)

        return ObjectFactory.resolve(self._node_type, operation_result.json())

    def create(self, json, **kwargs):
        json = json.to_json() if isinstance(json, NodeBase) else json
        operation_result = self._create_request("POST", self.url, json=json, **kwargs)

        return ObjectFactory.resolve(self._node_type, operation_result.json())

    def publish_node(self, node_resource, **kwargs):
        # ToDo: Validate that the `node_resource` is a draft
        # publishing the resource
        publish_node = node_resource.links["publish"]

        response = self._create_request("POST", publish_node, **kwargs)
        return ObjectFactory.resolve("NodeRecord", response.json())  # record is fixed here


class NodeFilesService(BaseService):

    def __init__(self, url: str, access_token: str, node_resource) -> None:
        super(NodeFilesService, self).__init__(url, access_token=access_token)

        if py_.is_none(node_resource.id):
            raise TypeError("The `node_resource` should be a defined Storm Service object.")

        self._node_resource = node_resource
        self._node_link_type = type(node_resource.links).__name__

    def _define_node_files(self, files, **kwargs):
        # preparing the files
        files = py_.map(files, lambda x: {"key": x} if isinstance(x, str) else x)
        files_link = py_.get(self._node_resource, "links.files", None)

        operation_result = self._create_request("POST", files_link, json=files, **kwargs)
        return operation_result.json()

    def upload_files(self, files, commit=False, **kwargs):
        # extracting files
        get_keys = lambda path: py_(self._node_resource).get(path).map(lambda x: x["key"]).value()
        node_resource_files = py_.interleave(get_keys("data.inputs"), get_keys("data.outputs"))

        # check if files is defined on record (to avoid API validation errors)
        intersected_files = py_.intersection(node_resource_files, files.keys())

        responses = []
        if intersected_files:
            defined_files = self._define_node_files(intersected_files)

            for defined_file in py_.get(defined_files, "entries", []):
                defined_file_key = defined_file["key"]
                defined_file_content_link = py_.get(defined_file, "links.content")

                # uploading the file
                file_to_upload = files.get(defined_file_key)

                response = asyncio.run(HTTPXClient.upload("PUT", defined_file_content_link, file_to_upload))
                responses.append(response)

                if commit:
                    response_json = response.json()

                    commit_url = py_.get(response_json, "links.commit")
                    self._create_request("POST", commit_url, json=files, **kwargs)

            return self._node_resource.links.self
        # ToDo: Improve exception handler
        raise FileNotFoundError("The defined files could not be sent to the service.")


__all__ = (
    "NodeService",
    "NodeFilesService"
)
