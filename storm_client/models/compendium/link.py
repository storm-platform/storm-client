#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import asyncio
from collections import UserDict

from pydash import py_

from ...network import HTTPXClient
from ...object_factory import ObjectFactory


#
# Compendium links
#
class CompendiumLink(UserDict):

    def __init__(self, typename, data=None):
        super(CompendiumLink, self).__init__(data or {})

        self.typename = typename

    def _check_property(self, property_path):
        if not py_.has(self, property_path):
            raise AttributeError(f"{property_path} attribute not available for this object!")

    def _resolve_link(self, property_path, http_method="GET", typename=None):
        self._check_property(property_path)

        # check if the type must be forced
        typename = typename if typename else self.typename

        # making the request
        response = asyncio.run(HTTPXClient.request(http_method, self[property_path])).json()

        if py_.has(response, "hits.hits"):  # for the `version` attribute
            return [
                ObjectFactory.resolve(typename, r) for r in py_.get(response, "hits.hits")
            ]

        if py_.has(response, "entries"):  # for the `files` attribute
            response = py_.get(response, "entries")

        return ObjectFactory.resolve(typename, response)

    @property
    def self(self):
        return self._resolve_link("self")

    @property
    def latest(self):
        return self._resolve_link("latest")

    @property
    def draft(self):
        raise NotImplementedError("You must use an implementation of the `CompendiumLink` class to access this operation.")

    @property
    def versions(self):
        return self._resolve_link("versions")

    @property
    def files(self):
        return self._resolve_link("files", http_method="GET", typename="CompendiumFiles")


class CompendiumDraftLink(CompendiumLink):
    def __init__(self, data=None):
        super(CompendiumDraftLink, self).__init__("CompendiumDraft", data or {})

    @property
    def draft(self):
        return self._resolve_link("draft", http_method="GET", typename="CompendiumDraft")


class CompendiumRecordLink(CompendiumLink):
    def __init__(self, data=None):
        super(CompendiumRecordLink, self).__init__("CompendiumRecord", data or {})

    @property
    def draft(self):
        return self._resolve_link("draft", http_method="POST", typename="CompendiumRecord")


__all__ = (
    "CompendiumLink",
    "CompendiumDraftLink",
    "CompendiumRecordLink"
)
