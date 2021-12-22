# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict

from typeguard import typechecked
from cachetools import LRUCache, cached

from .base import BaseService
from ..object_factory import ObjectFactory
from ..models.pipeline.model import Pipeline, PipelineList


@typechecked
class PipelineService(BaseService):
    """Research Pipeline service."""

    base_path = "pipelines"
    """Base service path in the Rest API."""

    def __init__(self, url: str) -> None:
        super(PipelineService, self).__init__(url, self.base_path)

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> PipelineList:
        """Search for Research pipelines.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            PipelineList: List with the founded Research Pipelines.
        """
        operation_result = self._create_request(
            "GET", self.url, params=kwargs, **request_options or {}
        )

        return ObjectFactory.resolve("PipelineList", operation_result.json())

    def create(self, pipeline: Pipeline, request_options: Dict = None) -> Pipeline:
        """Create a new Research Pipeline in the Storm WS.

        Args:
            pipeline (Pipeline): Pipeline object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Pipeline: Created Research Pipeline.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_result = self._create_request(
            "POST", self.url, json=pipeline, **request_options or {}
        )

        return ObjectFactory.resolve("Pipeline", operation_result.json())

    def get(self, pipeline_id: str, request_options: Dict = None) -> Pipeline:
        """Get an existing Research Pipeline from Storm WS.

        Args:
            pipeline_id (str): Pipeline ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Pipeline: Research Pipeline.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(pipeline_id)
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve("Pipeline", operation_result.json())

    def save(self, pipeline: Pipeline, request_options: Dict = None) -> Pipeline:
        """Update an existing Research Pipeline in the Storm WS.

        Args:
            pipeline (Pipeline): Pipeline object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Pipeline: Updated Research Pipeline.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(pipeline.id)
        operation_result = self._create_request(
            "PUT", operation_url, json=pipeline, **request_options or {}
        )

        return ObjectFactory.resolve("Pipeline", operation_result.json())

    def delete(self, pipeline_id, request_options: Dict = None):
        """Delete an existing Research Pipeline from Storm WS.

        Args:
            pipeline_id (str): Pipeline ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(pipeline_id)
        self._create_request("DELETE", operation_url, **request_options or {})

    def sync_compendia(
        self,
        pipeline: Pipeline,
        request_options: Dict = None,
    ):
        """Add an existing Research Compendium published (Record) to an Research Pipeline in the Storm WS.

        Args:
            pipeline (str): Pipeline object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        # now, we can send them!
        diff_values = list(pipeline.diff())

        added = (pipeline.links.actions.add_compendium, diff_values[0][1])
        removed = (pipeline.links.actions.delete_compendium, diff_values[1][1])

        # adding/removing compendia from the Storm WS
        for operation_base_url, compendia_list in [removed, added]:
            for cid in compendia_list:

                operation_url = f"{operation_base_url}/{cid}"

                operation_result = self._create_request(
                    "POST", operation_url, json=pipeline, **request_options or {}
                )
