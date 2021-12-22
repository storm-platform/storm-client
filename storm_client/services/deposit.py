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
from ..models.deposit import DepositList, Deposit
from ..object_factory import ObjectFactory


@typechecked
class DepositService(BaseService):
    """Deposit service."""

    base_path = "deposits"
    """Base service path in the Rest API."""

    def __init__(self, url: str) -> None:
        super(DepositService, self).__init__(url, self.base_path)

    def list_services(self, request_options: Dict = None):
        """List all available deposit services.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            DepositServiceList: List with the founded Deposits services.
        """
        operation_url = self._build_url("services")
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve("DepositServiceList", operation_result.json())

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> DepositList:
        """Search for deposits in the Storm WS.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            DepositList: List with the founded Deposits.
        """
        operation_result = self._create_request(
            "GET", self.url, params=kwargs, **request_options or {}
        )

        return ObjectFactory.resolve("DepositList", operation_result.json())

    def create(self, deposit: Deposit, request_options: Dict = None) -> Deposit:
        """Create a new Deposit request in the Storm WS.

        Args:
            deposit (Deposit): Deposit object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Created Deposit request.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_result = self._create_request(
            "POST", self.url, json=deposit, **request_options or {}
        )

        return ObjectFactory.resolve("Deposit", operation_result.json())

    def get(self, deposit_id: str, request_options: Dict = None) -> Deposit:
        """Get an existing Deposit request from Storm WS.

        Args:
            deposit_id (str): Deposit ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Deposit object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(deposit_id)
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve("Deposit", operation_result.json())

    def save(self, deposit: Deposit, request_options: Dict = None) -> Deposit:
        """Update an existing Deposit request in the Storm WS.

        Args:
            deposit (Deposit): Pipeline object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Deposit: Updated Deposit request.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(deposit.id)
        operation_result = self._create_request(
            "PUT", operation_url, json=deposit, **request_options or {}
        )

        return ObjectFactory.resolve("Deposit", operation_result.json())

    def delete(self, deposit_id, request_options: Dict = None):
        """Delete an existing Deposit request from the Storm WS.

        Args:
            deposit_id (str): Deposit ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(deposit_id)
        self._create_request("DELETE", operation_url, **request_options or {})
