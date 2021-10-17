#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager services accessor."""
from .services.accessor import NodeAccessor
from .services.project import ProjectService


class Storm:
    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token

    @property
    def project(self):
        return ProjectService(self._url, self._access_token)

    @property
    def node(self):
        return NodeAccessor(self._url, self._access_token)


__all__ = (
    "Storm"
)
