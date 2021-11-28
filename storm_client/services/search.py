# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import posixpath

from pydash import py_

from .base import BaseService
from ..models import CompendiumRecordList
from ..object_factory import ObjectFactory

from typing import Dict
from typeguard import typechecked

from cachetools import cached, LRUCache


@typechecked
class CompendiumSearchService(BaseService):
    def __init__(
        self, url: str, access_token: str, project_id: str, user_records: bool = False
    ) -> None:
        self._base_path = posixpath.join("projects", project_id, "compendia")

        if user_records:
            self._base_path = posixpath.join("user", self._base_path)

        super(CompendiumSearchService, self).__init__(
            url, self._base_path, access_token
        )

    @cached(cache=LRUCache(maxsize=128))
    def query(self, request_options: Dict = {}, **kwargs) -> CompendiumRecordList:
        operation_result = self._create_request(
            "GET", self.url, params=kwargs, **request_options
        )

        return ObjectFactory.resolve(
            "CompendiumRecordList", py_.get(operation_result.json(), "hits.hits", {})
        )


__all__ = "CompendiumSearchService"
