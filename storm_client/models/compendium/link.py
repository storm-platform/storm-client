# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from ..base import BaseModel
from ...network import HTTPXClient
from ...object_factory import ObjectFactory


class BaseCompendiumLink(BaseModel):
    """Base Compendium link class."""

    def __init__(self, typename, data=None):
        super(BaseCompendiumLink, self).__init__(data or {})
        self.typename = typename

    def _resolve_link(self, field_path, http_method="GET", typename=None):
        """Resolve a link into an available storm-client data class."""
        self.has_field(field_path)

        # defining the typename used to materialize
        # the data extracted from the service.
        typename = typename if typename else self.typename

        response = HTTPXClient.request(http_method, self[field_path]).json()
        if py_.has(response, "hits.hits"):  # for the `version` attribute
            return [
                ObjectFactory.resolve(typename, r)
                for r in py_.get(response, "hits.hits")
            ]

        return ObjectFactory.resolve(typename, response)

    @property
    def files(self):
        """Compendium `files` link."""
        return self._resolve_link(
            "files", http_method="GET", typename="CompendiumFiles"
        )


class CompendiumRecordLink(BaseCompendiumLink):
    """Compendium Record (Published) link class."""

    def __init__(self, data=None):
        super(CompendiumRecordLink, self).__init__("CompendiumRecord", data or {})

    @property
    def self(self):
        """Compendium `self` link."""
        return self._resolve_link("self")

    @property
    def latest(self):
        """Compendium `latest` version link."""
        return self._resolve_link("latest")

    @property
    def versions(self):
        """Compendium `versions` link."""
        return self._resolve_link("versions")


class CompendiumDraftLink(BaseCompendiumLink):
    """Compendium Draft (Not published) link class."""

    def __init__(self, data=None):
        super(CompendiumDraftLink, self).__init__("CompendiumDraft", data or {})

    @property
    def self(self):
        """Compendium `self` link.

        Note:
            In the case of Compendium Draft, the link ``draft`` is used.
        """
        return self._resolve_link("draft")
