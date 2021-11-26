# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import asyncio
import posixpath

from pydash import py_

from ..network import HTTPXClient


class BaseService:
    def __init__(
        self,
        service_url: str,
        base_path: str = None,
        access_token: str = None,
        **kwargs
    ) -> None:
        self._base_path = base_path
        self._service_url = service_url
        self._access_token = access_token

        self._access_token_as_parameter = {"access_token": self._access_token}

    @property
    def url(self):
        if not self._base_path:
            raise NotImplemented(
                "This method is implemented to use `service_url` and `base_path`."
            )

        return posixpath.join(self._service_url, self._base_path)

    @property
    def access_token(self):
        return self._access_token

    def _build_url(self, urls):
        return posixpath.join(*[self.url, *urls]).strip("/")

    def _create_request(self, method, url, **kwargs):
        response = asyncio.run(
            HTTPXClient.request(
                method,
                url,
                **py_.merge(kwargs, {"params": self._access_token_as_parameter})
            ),
        )
        response.raise_for_status()

        return response


__all__ = "BaseService"
