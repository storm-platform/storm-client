#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager services accessor."""

from storm_client.services.project import ProjectService
from storm_client.services.node import NodeService, NodeFilesService


class Storm:
    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token

    @property
    def project(self):
        return ProjectService(self._url, self._access_token)

    def node_draft(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=True)

    def node_record(self, project_id):
        return NodeService(self._url, self._access_token, project_id, as_draft=False)

    def node_files(self, node_resource):
        return NodeFilesService(self._url, self._access_token, node_resource)
