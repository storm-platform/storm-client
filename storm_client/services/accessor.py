# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .search import CompendiumSearchService
from .compendium import CompendiumService, CompendiumFilesService


class BaseServiceAccessor:
    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token


class CompendiumAccessor(BaseServiceAccessor):
    def __init__(self, url, access_token):
        super(CompendiumAccessor, self).__init__(url, access_token)

    def draft(self, project_id):
        return CompendiumService(
            self._url, self._access_token, project_id, as_draft=True
        )

    def record(self, project_id):
        return CompendiumService(
            self._url, self._access_token, project_id, as_draft=False
        )

    def files(self, node_resource):
        return CompendiumFilesService(self._url, self._access_token, node_resource)

    def search(self, project_id, user_records=False):
        return CompendiumSearchService(
            self._url, self._access_token, project_id, user_records
        )


__all__ = ("CompendiumAccessor", "BaseServiceAccessor")
