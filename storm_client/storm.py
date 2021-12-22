# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager services accessor."""

from .store import TokenStore
from .network import HTTPXClient
from .services.project import ProjectService


class Storm:
    """SpatioTemporal Open Research Manager Client."""

    def __init__(self, url, access_token, **kwargs):
        """Initializer.

        Args:
            url (str): Storm WS service URL.

            access_token (str): Token to access the Storm WS.

            kwargs (dict): Optional parameters to the ``httpx.Client``.

        See:
            For more details about the ``httpx.Client``, please check the
            official documentation: https://www.python-httpx.org/api/#client
        """
        self._url = url

        # saving the token in the store.
        # this is the only one entry point
        # of the store.
        TokenStore.save_token(access_token)

        if kwargs:
            HTTPXClient.set_client_config(kwargs)

    @property
    def project(self):
        """Storm Project entrypoint."""
        return ProjectService(self._url)

    @property
    def is_connected(self):
        """Check connection with the Storm WS."""
        is_ok = True
        try:
            HTTPXClient.request("GET", self._url)
        except:  # noqa
            is_ok = False
        return is_ok
