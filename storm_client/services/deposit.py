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
from ..models.deposit import DepositJobList, DepositJob
from ..models.extractor import IDExtractor
from ..object_factory import ObjectFactory


@typechecked
class DepositJobService(RecordOperatorService):
    """Deposit service."""

    base_path = "deposits"
    """Base service path in the Rest API."""

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> DepositJobList:
        """Search for deposit jobs in the Storm WS.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            DepositList: List with the founded Deposits.
        """
        return self._create_op_search("DepositJobList", request_options, **kwargs)

    def create(self, deposit: DepositJob, request_options: Dict = None) -> DepositJob:
        """Create a new Deposit request in the Storm WS.

        Args:
            deposit (DepositJob): Deposit Job object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Created Deposit request.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_create(deposit, "DepositJob", request_options)

    def get(
        self, deposit: Union[str, DepositJob], request_options: Dict = None
    ) -> DepositJob:
        """Get an existing Deposit Job request from Storm WS.

        Args:
            deposit (str):  Deposit Job ID or Deposit Job object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Deposit object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_get(
            IDExtractor.extract(deposit), "DepositJob", request_options
        )

    def save(self, deposit: DepositJob, request_options: Dict = None) -> DepositJob:
        """Update an existing Deposit request in the Storm WS.

        Args:
            deposit (DepositJob): Deposit Job object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Updated Deposit request.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_save(deposit, "DepositJob", request_options)

    def delete(self, deposit: Union[str, DepositJob], request_options: Dict = None):
        """Delete an existing Deposit Job request from the Storm WS.

        Args:
            deposit (Union[str, Deposit]): Deposit Job ID or Deposit Job object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_delete(IDExtractor.extract(deposit), request_options)

    def list_services(self, request_options: Dict = None):
        """List all available deposit services.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            DepositServiceList: List with the founded Deposits services.
        """
        operation_url = self._build_url("services")
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve("DepositJobServiceList", operation_result.json())

    def start_deposit(self, deposit: Union[str, DepositJob], request_options: Dict = None):
        """Start an existing Deposit in the Storm WS.

        Args:
            deposit (Union[str, Deposit]): Deposit ID or Deposit object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Updated Deposit.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(deposit), "actions/start", "POST", request_options
        )

        return self.get(deposit)

    def cancel_deposit(
        self, deposit: Union[str, DepositJob], request_options: Dict = None
    ):
        """Cancel an existing Deposit Job (In progress) in the Storm WS.

        Args:
            deposit (Union[str, DepositJob]): Deposit Job ID or Deposit Job object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Updated Deposit.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(deposit), "actions/cancel", "POST", request_options
        )

        return self.get(deposit)
