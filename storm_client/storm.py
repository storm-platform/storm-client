# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager services accessor."""

from .services.project import ProjectService
from .services.accessor import CompendiumAccessor


class Storm:
    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token

    @property
    def project(self):
        return ProjectService(self._url, self._access_token)

    @property
    def compendium(self):
        return CompendiumAccessor(self._url, self._access_token)


__all__ = "Storm"
