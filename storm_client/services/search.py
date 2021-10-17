#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import posixpath

from pydash import py_

from .base import BaseService
from ..models import NodeRecordList
from ..object_factory import ObjectFactory

from typing import Dict
from typeguard import typechecked

from cachetools import cached, LRUCache


@typechecked
class NodeSearchService(BaseService):
    def __init__(self, url: str, access_token: str, project_id: int, user_records: bool = False) -> None:
        self._base_path = posixpath.join("graph", str(project_id), "node")

        if user_records:
            self._base_path = posixpath.join("user", self._base_path)

        super(NodeSearchService, self).__init__(url, self._base_path, access_token)

    @cached(cache=LRUCache(maxsize=128))
    def query(self, request_options: Dict = {}, **kwargs) -> NodeRecordList:
        operation_result = self._create_request("GET", self.url, params=kwargs, **request_options)

        return ObjectFactory.resolve("NodeRecordList", py_.get(operation_result.json(), "hits.hits", {}))


__all__ = (
    "NodeSearchService"
)
