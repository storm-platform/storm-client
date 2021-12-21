# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import httpx
import aiofiles
from pydash import py_

from .store import TokenStore
from .io import file_chunks_generator


class HTTPXClient:

    _client_config = {"timeout": 12, "verify": False}
    """Default client config."""

    @classmethod
    def _proxy_request(cls, request_options):
        """Proxy a request to add the authentication access token."""

        # proxing the request with the authentication header
        service_access_token = TokenStore.get_token()

        if service_access_token:
            request_options = py_.merge(
                request_options or {}, {"headers": {"x-api-key": service_access_token}}
            )
        return request_options

    @classmethod
    def set_client_config(cls, configuration):
        """Define the configuration for the ``httpx.Client``.

        Args:
            configuration (dict): ``httpx.Client`` configuration

        See:
            For more details about the ``httpx.Client``, please check the
            official documentation: https://www.python-httpx.org/api/#client
        """
        cls._client_config = configuration

    @classmethod
    def request(cls, method, url, **kwargs):
        """Synchronous HTTP request.

        Request an URL using the specified HTTP ``method``.
        Args:
            method (str): HTTP Method used to request (e.g. `GET`, `POST`, `PUT`, `DELETE`)

            url (str): URL that will be requested

            **kwargs (dict): Extra parameters to `httpx.request` method.

        Returns:
            httpx.Response: Request response.

        See:
            This method is built on top of ``httpx``. For more details of options available, please,
            check the official documentation: https://www.python-httpx.org/
        """
        with httpx.Client(**cls._client_config) as client:
            return client.request(method, url, **cls._proxy_request(kwargs or {}))

    @classmethod
    async def download(cls, url: str, output_file: str, **kwargs):
        """Download a file.

        Args:
            url (str): File URL.

            output_file (str): Path where the file will be saved.

            kwargs (dict): Extra parameters to ``http.AsyncClient.stream``.

        Returns:
            str: The path to the downloaded file.

        See:
            For more details about ``http.AsyncClient.stream`` options, please check
            the official documentation: https://www.python-httpx.org/api/#asyncclient
        """
        request_args = cls._proxy_request(kwargs)

        async with httpx.AsyncClient(**cls._client_config) as client:
            async with client.stream("GET", url, **request_args) as response:
                async with aiofiles.open(output_file, "wb") as ofile:
                    async for chunk in response.aiter_bytes():
                        await ofile.write(chunk)
        return output_file

    @staticmethod
    def upload(method, url, file_path, **kwargs):
        """Download a file.

        Args:

            method (str): HTTP verb used to upload the data.

            url (str): URL to send the data.

            file_path (str): File path.

            kwargs (dict): Extra parameters to ``http.Client.request``.

        Returns:
            httpx.Response: Request response.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return HTTPXClient.request(
            method=method, url=url, data=file_chunks_generator(file_path), **kwargs
        )
