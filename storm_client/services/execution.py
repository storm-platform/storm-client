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
from ..models.execution.model import ExecutionJobList, ExecutionJob
from ..object_factory import ObjectFactory


@typechecked
class ExecutionService(RecordOperatorService):
    """Execution service."""

    base_path = "executions"
    """Base service path in the Rest API."""

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> ExecutionJobList:
        """Search for jobs in the Storm WS.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            JobList: List with the founded Jobs.
        """
        return self._create_op_search("ExecutionJobList", request_options, **kwargs)

    def create(self, job: ExecutionJob, request_options: Dict = None) -> ExecutionJob:
        """Create a new Execution Job in the Storm WS.

        Args:
            job (ExecutionJob): Job object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Job: Created Job request.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_create(job, "ExecutionJob", request_options)

    def get(self, job: Union[str, ExecutionJob], request_options: Dict = None) -> ExecutionJob:
        """Get an existing Execution Job from Storm WS.

        Args:
            job (Union[str, ExecutionJob]): Job ID or Job record.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Job: Job object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_get(IDExtractor.extract(job), "ExecutionJob", request_options)

    def save(self, job: ExecutionJob, request_options: Dict = None) -> ExecutionJob:
        """Update an existing Execution Job in the Storm WS.

        Args:
            job (ExecutionJob): Job object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Job: Updated Execution Job.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_save(job, "ExecutionJob", request_options)

    def delete(self, job: Union[str, ExecutionJob], request_options: Dict = None):
        """Delete an existing Execution Job from the Storm WS.

        Args:
            job (Union[str, ExecutionJob]): Job ID or Job record.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_delete(IDExtractor.extract(job), request_options)

    def list_services(self, request_options: Dict = None):
        """List all jobs services available.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            JobServiceList: List with the founded Job services.
        """
        operation_url = self._build_url("services")
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve("ExecutionJobServiceList", operation_result.json())

    def start_job(self, job: Union[str, ExecutionJob], request_options: Dict = None):
        """Start an existing Execution Job in the Storm WS.

        Args:
            job (Union[str, ExecutionJob]): Job ID or Job object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Job: Updated Execution Job.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(job), "actions/start", "POST", request_options
        )

        return self.get(job)

    def cancel_job(self, job: Union[str, ExecutionJob], request_options: Dict = None):
        """Cancel an Execution Job (In execution) in the Storm WS.

        Args:
            job (Union[str, ExecutionJob]): Job ID or Job object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Job: Updated Execution Job.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(job), "actions/cancel", "POST", request_options
        )

        return self.get(job)
