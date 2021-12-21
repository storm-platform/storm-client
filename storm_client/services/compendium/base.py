# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typeguard import typechecked

from ...services.base import BaseService


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
