#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from typing import Union

import posixpath

from pydash import py_
from cachetools import cached, LRUCache

from storm_client.models.node import NodeBase
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


__all__ = (
    "NodeService"
)
