# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Union, Dict

from typeguard import typechecked

from ..base import BaseRecordHandlerService
from ...models.compendium import CompendiumBase
from ...object_factory import ObjectFactory


@typechecked
class BaseCompendiumService(BaseRecordHandlerService):
    """Base Execution Compendium service."""

    base_path = "compendia"
    """Base service path in the Rest API."""

    compendium_type = ""
    """Compendium type"""

    complement_url = ""
    """Complement URL type"""

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
