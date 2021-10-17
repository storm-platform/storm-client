#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from .search import NodeSearchService
from .node import NodeService, NodeFilesService


class BaseServiceAccessor:

    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token


class NodeAccessor(BaseServiceAccessor):

    def __init__(self, url, access_token):
        super(NodeAccessor, self).__init__(url, access_token)

    def draft(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=True)

    def record(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=False)

    def files(self, node_resource):
        return NodeFilesService(self._url, self._access_token, node_resource)

    def search(self, project_id, user_records=False):
        return NodeSearchService(self._url, self._access_token, project_id, user_records)


__all__ = (
    "NodeAccessor",
    "BaseServiceAccessor"
)
