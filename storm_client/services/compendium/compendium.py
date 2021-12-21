# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict, Union
from typeguard import typechecked

from .base import BaseCompendiumService
from ...models.compendium import (
    CompendiumDraft,
    CompendiumRecord,
    CompendiumBase,
)
from ...object_factory import ObjectFactory


@typechecked
class BaseCompendiumHandlerService(BaseCompendiumService):
    """Base compendium handler service."""

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


@typechecked
class CompendiumRecordService(BaseCompendiumHandlerService):
    """Execution Compendium (Record) service."""

    compendium_type = "CompendiumRecord"
    """Compendium type"""

    def new_version(
        self, compendium: CompendiumRecord, request_options: Dict = None
    ) -> CompendiumDraft:
        """Crate a new Compendium Draft from an existing Compendium Record.

        Args:
            compendium (CompendiumRecord): Compendium Record object from which the
                                           draft will be created.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Created Compendium Draft.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_data_handle_request(
            compendium, "links.versions", "POST", "CompendiumDraft", request_options
        )


@typechecked
class CompendiumDraftService(BaseCompendiumHandlerService):
    """Execution Compendium (Draft) service."""

    compendium_type = "CompendiumDraft"
    """Compendium type"""

    complement_url = "draft"
    """Complement URL type"""

    def create(
        self, compendium: CompendiumDraft, request_options: Dict = None
    ) -> CompendiumDraft:
        """Create a new Execution Compendium (Draft) in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Execution Compendium Draft.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_result = self._create_request(
            "POST", self.url, json=compendium, **request_options or {}
        )

        return ObjectFactory.resolve(self.compendium_type, operation_result.json())

    def save(self, compendium: CompendiumDraft, request_options: Dict = None):
        """Update an existing Compendium Draft in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object to save in the service.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Saved Compendium Draft.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_data_handle_request(
            compendium, "links.self", "PUT", "CompendiumDraft", request_options or {}
        )

    def publish(
        self, compendium: CompendiumDraft, request_options: Dict = None
    ) -> CompendiumRecord:
        """Publish an existing Compendium Draft in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Created Research Project.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client

        Note:
            This action will publish the Compendium Draft, making a new Compendium Record,
            which is available to other users in the project
        """
        return self._create_data_handle_request(
            compendium,
            "links.publish",
            "POST",
            "CompendiumRecord",
            request_options or {},
        )
