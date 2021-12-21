# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import posixpath
import simplejson

from ..network import HTTPXClient


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
