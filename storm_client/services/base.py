# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import posixpath
from typing import Dict

import simplejson

from ..models.base import BaseModel
from ..network import HTTPXClient
from ..object_factory import ObjectFactory


class BaseService:
    """Base service class.

    This class provides useful methods to handle web services
    urls and request/responses.
    """

    base_path = "<path>"
    """Base service path in the Rest API."""

    @property
    def url(self):
        if not self._base_path:
            return self._service_url
        return posixpath.join(self._service_url, self._base_path)

    def __init__(self, service_url: str, base_path: str = None, **kwargs) -> None:
        self._base_path = base_path
        self._service_url = service_url

    def _build_url(self, paths):
        """Create a valid url based on a list of paths."""
        if not isinstance(paths, list):
            # trying "cast" the argument to a list
            # to avoid posixpath errors
            paths = [paths]
        return posixpath.join(*[self.url, *paths]).strip("/")

    def _create_request(self, method, url, raise_exception=True, **kwargs):
        """Create a request and check errors in the response."""

        # special request: if a ``json`` field is defined,
        # we serialize it assuming that is a storm-client data model.
        if "json" in kwargs:
            kwargs["json"] = simplejson.loads(
                simplejson.dumps(kwargs.get("json", {}), for_json=True)
            )

        response = HTTPXClient.request(method, url, **kwargs or {})

        if raise_exception:
            response.raise_for_status()
        return response


class BaseRecordHandlerService(BaseService):
    """Base record service for record handle in the Storm WS.

    This class provides useful methods to manipulate records
    in the Storm WS.
    """

    def __init__(self, url: str) -> None:
        super(BaseRecordHandlerService, self).__init__(url, self.base_path)

    def _create_data_handle_request(
        self,
        data: BaseModel,
        link_path: str,
        method: str,
        request_options: Dict = None,
    ):
        """Create a request record data handle.

        This is a generic method that receives a description of the request to do.
        The method manipulates the record data and creates the request based on the
        link system provided by the service.
        Args:
            data (BaseModel): Record object with valid links.

            link_path (str): Field path of the record data where link
                             used in operation will be extracted from.

            method (str): HTTP Method used in the request.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Dict: request data result.
        """
        # getting the link to save the draft
        operation_url = data.get_field(link_path)

        # make the request!
        operation_result = self._create_request(
            method, operation_url, json=data, **request_options or {}
        )

        return operation_result.json()

    def _create_op_search(
        self, result_type: str, request_options: Dict = None, **kwargs
    ):
        """Search for records in the Storm WS.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            ``result_type``: List with the founded records.
        """
        operation_result = self._create_request(
            "GET", self.url, params=kwargs, **request_options or {}
        )

        return ObjectFactory.resolve(result_type, operation_result.json())

    def _create_op_create(self, data, result_type: str, request_options=None):
        """Create a new Record in the Storm WS.

        Args:
            data (BaseModel): Record data.

            kwargs (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            ``result_type``: Created Record.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_result = self._create_request(
            "POST", self.url, json=data, **request_options or {}
        )

        return ObjectFactory.resolve(result_type, operation_result.json())

    def _create_op_get(
        self, record_id: str, result_type: str, request_options: Dict = None
    ):
        """Get an existing Record from Storm WS.

        Args:
            record_id (str): Record ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            ``result_type``: Record object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(record_id)
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve(result_type, operation_result.json())

    def _create_op_save(self, data, result_type: str, request_options: Dict = None):
        """Update an existing Record in the Storm WS.

        Args:
            data (BaseModel): Record object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            ``result_type``: Updated Record object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(data.id)
        operation_result = self._create_request(
            "PUT", operation_url, json=data, **request_options or {}
        )

        return ObjectFactory.resolve(result_type, operation_result.json())

    def _create_op_delete(self, record_id, request_options: Dict = None):
        """Delete an existing Record from the Storm WS.

        Args:
            record_id (str): Record ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_url = self._build_url(record_id)
        self._create_request("DELETE", operation_url, **request_options or {})
