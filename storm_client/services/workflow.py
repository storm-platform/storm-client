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
from ..models.workflow.model import Workflow, WorkflowList


@typechecked
class WorkflowService(RecordOperatorService):
    """Research Workflow service."""

    base_path = "workflows"
    """Base service path in the Rest API."""

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> WorkflowList:
        """Search for Research Workflows.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            WorkflowList: List with the founded Research Workflows.
        """
        return self._create_op_search("WorkflowList", request_options, **kwargs)

    def create(self, workflow: Workflow, request_options: Dict = None) -> Workflow:
        """Create a new Research Workflow in the Storm WS.

        Args:
            workflow (Workflow): Workflow object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Workflow: Created Research Workflow.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_create(workflow, "Workflow", request_options)

    def get(
        self, workflow: Union[str, Workflow], request_options: Dict = None
    ) -> Workflow:
        """Get an existing Research Workflow from Storm WS.

        Args:
            workflow (Union[str, Workflow]): Workflow ID or Workflow object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Workflow: Research Workflow.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_get(
            IDExtractor.extract(workflow), "Workflow", request_options
        )

    def save(self, workflow: Workflow, request_options: Dict = None) -> Workflow:
        """Update an existing Research Workflow in the Storm WS.

        Args:
            workflow (Workflow): Workflow object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Workflow: Updated Research Workflow.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_save(workflow, "Workflow", request_options)

    def delete(self, workflow: Union[str, Workflow], request_options: Dict = None):
        """Delete an existing Research Workflow from Storm WS.

        Args:
            workflow (Union[str, Workflow]): Workflow ID or Workflow object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_delete(IDExtractor.extract(Workflow), request_options)

    def sync_compendia(
        self,
        workflow: Workflow,
        request_options: Dict = None,
    ):
        """Synchronize a local Research Workflow Graph with the Storm WS.

        This method calculates the difference between the ``workflow graph`` defined by the user
        with it original version (Loaded from the server). The differences (additions and removals)
        are synchronized.
        Args:

            workflow (Workflow): Workflow object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        diff_values = list(workflow.diff())

        added = ("POST", workflow.links.actions.add_compendium, diff_values[0][1])
        removed = (
            "DELETE",
            workflow.links.actions.delete_compendium,
            diff_values[1][1],
        )

        # adding/removing compendia from the Storm WS
        for method, operation_base_url, compendia_list in [removed, added]:
            for cid in compendia_list:

                operation_url = f"{operation_base_url}/{cid}"

                self._create_request(
                    method, operation_url, json=workflow, **request_options or {}
                )

        # reload the object from the server.
        return workflow.links.self

    def finalize(self, workflow: Union[str, Workflow], request_options: Dict = None):
        """Finalize an existing Research Workflow in the Storm WS.

        Args:
            workflow (Union[str, Workflow]): Workflow ID or Workflow object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Workflow: Updated Research Workflow.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(workflow), "actions/finish", "POST", request_options
        )

        return self.get(workflow)
