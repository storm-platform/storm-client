# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict, Union

from cachetools import LRUCache, cached
from typeguard import typechecked

from .base import RecordOperatorService
from ..models.extractor import IDExtractor
from ..models.pipeline.model import Pipeline, PipelineList


@typechecked
class PipelineService(RecordOperatorService):
    """Research Pipeline service."""

    base_path = "pipelines"
    """Base service path in the Rest API."""

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> PipelineList:
        """Search for Research pipelines.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            PipelineList: List with the founded Research Pipelines.
        """
        return self._create_op_search("PipelineList", request_options, **kwargs)

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
        return self._create_op_create(pipeline, "Pipeline", request_options)

    def get(
        self, pipeline: Union[str, Pipeline], request_options: Dict = None
    ) -> Pipeline:
        """Get an existing Research Pipeline from Storm WS.

        Args:
            pipeline (Union[str, Pipeline]): Pipeline ID or Pipeline object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Pipeline: Research Pipeline.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_get(
            IDExtractor.extract(pipeline), "Pipeline", request_options
        )

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
        return self._create_op_save(pipeline, "Pipeline", request_options)

    def delete(self, pipeline: Union[str, Pipeline], request_options: Dict = None):
        """Delete an existing Research Pipeline from Storm WS.

        Args:
            pipeline (Union[str, Pipeline]): Pipeline ID or Pipeline object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_delete(IDExtractor.extract(pipeline), request_options)

    def sync_compendia(
        self,
        pipeline: Pipeline,
        request_options: Dict = None,
    ):
        """Synchronize a local Research Pipeline Graph with the Storm WS.

        This method calculates the difference between the ``pipeline graph`` defined by the user
        with it original version (Loaded from the server). The differences (additions and removals)
        are synchronized.
        Args:

            pipeline (Pipeline): Pipeline object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        diff_values = list(pipeline.diff())

        added = ("POST", pipeline.links.actions.add_compendium, diff_values[0][1])
        removed = (
            "DELETE",
            pipeline.links.actions.delete_compendium,
            diff_values[1][1],
        )

        # adding/removing compendia from the Storm WS
        for method, operation_base_url, compendia_list in [removed, added]:
            for cid in compendia_list:

                operation_url = f"{operation_base_url}/{cid}"

                self._create_request(
                    method, operation_url, json=pipeline, **request_options or {}
                )

        # reload the object from the server.
        return pipeline.links.self

    def finalize(self, pipeline: Union[str, Pipeline], request_options: Dict = None):
        """Finalize an existing Research Pipeline in the Storm WS.

        Args:
            pipeline (Union[str, Pipeline]): Pipeline ID or Pipeline object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Pipeline: Updated Research Pipeline.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(pipeline), "actions/finish", "POST", request_options
        )

        return self.get(pipeline)
