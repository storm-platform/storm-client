#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import asyncio
import posixpath

from storm_client.network import HTTPXClient


class BaseService:

    def __init__(self, service_url: str, base_path: str, access_token: str) -> None:
        self._base_path = base_path
        self._service_url = service_url
        self._access_token = access_token

        self._access_token_as_parameter = {"access_token": self._access_token}

    @property
    def url(self):
        return posixpath.join(self._service_url, self._base_path)

    @property
    def access_token(self):
        return self._access_token

    def _build_url(self, urls):
        return posixpath.join(*[self.url, *urls]).strip("/")

    def _create_request(self, method, url, **kwargs):
        return asyncio.run(HTTPXClient.request(method, url, params=self._access_token_as_parameter, **kwargs))


__all__ = (
    "BaseService"
)
