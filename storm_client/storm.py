#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager services accessor."""

from cachetools import cached, LRUCache

from storm_client.services.node import NodeService
from storm_client.services.project import ProjectService


class Storm:
    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token

    @property
    @cached(cache=LRUCache(maxsize=1))
    def project(self):
        return ProjectService(self._url, self._access_token)

    @cached(cache=LRUCache(maxsize=1))
    def node_draft(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=True)

    @cached(cache=LRUCache(maxsize=1))
    def node_record(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=False)
