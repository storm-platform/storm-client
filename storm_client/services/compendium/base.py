# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict, Union
from typeguard import typechecked

from ...services.base import BaseService
from ...object_factory import ObjectFactory
from ...models.compendium import (
    CompendiumBase,
    CompendiumDraft,
)


@typechecked
class BaseCompendiumService(BaseService):
    """Base Execution Compendium service."""

    base_path = "compendia"
    """Base service path in the Rest API."""

    compendium_type = ""
    """Compendium type"""

    complement_url = ""
    """Complement URL type"""

    def __init__(self, url: str) -> None:
        """Initializer.

        Args:
            url (str): Compendia services URL.

        Note:
            In the ``Draft`` mode only the draft compendia is available.
        """
        super(BaseCompendiumService, self).__init__(url, self.base_path)

    def get(
        self, compendium_id: str, request_options: Dict = None
    ) -> Union[CompendiumBase, None]:
        """Get an existing Research Project from Storm WS.

        Args:
            compendium_id (str): Compendium ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Created Research Project.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        # building the request url
        operation_url = self._build_url([compendium_id, self.complement_url])

        # get the defined compendia
        operation_result = self._create_request(
            "GET", operation_url, **request_options or {}
        )

        return ObjectFactory.resolve(self.compendium_type, operation_result.json())

    def _create_data_handle_request(
        self,
        compendium: CompendiumBase,
        link_path: str,
        method: str,
        result_type: str,
        request_options: Dict = None,
    ):
        """Create a request to handle the compendium data.

        This is a generic method that receives a description of the request to do.
        The method manipulates the compendium data and creates the request based on
        the information received.
        Args:
            compendium (CompendiumDraft): Compendium object to be created in the Storm WS.

            link_path (str): Path in the compendium data of the field with the link where the
                            request will be sent.

            method (str): HTTP Method (or verb) used in the request.

            result_type (str): Output data type. Must be a valid and registered
                               class in the ``ObjectFactory``

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            ``result_type``: Object with the data returned by the service.
        """

        # getting the link to save the draft
        operation_url = compendium.get_field(link_path)

        # save the compendium
        operation_result = self._create_request(
            method, operation_url, json=compendium, **request_options
        )

        # Factoring!
        return ObjectFactory.resolve(result_type, operation_result.json())
