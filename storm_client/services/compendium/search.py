# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import posixpath
from cachetools import LRUCache, cached

from typing import Dict
from typeguard import typechecked

from .base import BaseCompendiumService
from ...object_factory import ObjectFactory
from ...models.compendium import (
    CompendiumRecordList,
)


@typechecked
class CompendiumSearchService(BaseCompendiumService):
    """Execution Compendium Search service."""

    @cached(cache=LRUCache(maxsize=128))
    def search(
        self, user_records: bool = False, request_options: Dict = None, **kwargs
    ) -> CompendiumRecordList:
        """Search for Execution compendia.

        Args:
            user_records (bool): Flag indicating if the ``user context`` mode must be used.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            CompendiumRecordList: List with the founded Execution Compendia.

        Note:
            In the ``user context`` only the compendia created by the user is
            available.
        """
        # special case: the user workspace is defined by a "user" path before the
        # compendia url
        operation_url = (
            posixpath.join(self._service_url, self._base_path)
            if user_records
            else self.url
        )

        # search compendia
        operation_result = self._create_request(
            "GET", operation_url, params=kwargs, **request_options or {}
        )

        return ObjectFactory.resolve("CompendiumRecordList", operation_result.json())

    def __call__(
        self, user_records: bool = False, request_options: Dict = None, **kwargs
    ) -> CompendiumRecordList:
        """Search for Execution compendia.

        Args:
            user_records (bool): Flag indicating if the ``user context`` mode must be used.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            CompendiumRecordList: List with the founded Execution Compendia.

        Note:
            In the ``user context`` only the compendia created by the user is
            available.
        """
        return self.search(user_records, request_options, **kwargs)
