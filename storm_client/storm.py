# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager services accessor."""


from .network import HTTPXClient
from .store import TokenStore
from .services.project import ProjectService


class Storm:
    """SpatioTemporal Open Research Manager Client."""

    def __init__(self, url, access_token, **client_options):
        """Initializer.

        Args:
            url (str): Storm WS service URL.

            access_token (str): Token to access the Storm WS.

            client_options (dict): Optional parameters to the `httpx.Client`.
        """
        self._url = url

        # saving the token in the store.
        # this is the only one entry point
        # of the store.
        TokenStore.save_token(access_token)

        if client_options:
            HTTPXClient.set_client_config(client_options)

    @property
    def project(self):
        return ProjectService(self._url)
