# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ..link import resolve_link


class BaseCompendiumLink(BaseModel):
    """Base Compendium link class."""

    def __init__(self, typename, data=None):
        super(BaseCompendiumLink, self).__init__(data or {})
        self.typename = typename

    @property
    def files(self):
        """Compendium `files` link."""
        return resolve_link(self, "files", typename="CompendiumFiles")


class CompendiumRecordLink(BaseCompendiumLink):
    """Compendium Record (Published) link class."""

    def __init__(self, data=None):
        super(CompendiumRecordLink, self).__init__("CompendiumRecord", data or {})

    @property
    def self(self):
        """Compendium `self` link."""
        return resolve_link(self, "self", typename=self.typename)

    @property
    def latest(self):
        """Compendium `latest` version link."""
        return resolve_link(self, "latest", typename=self.typename)

    @property
    def versions(self):
        """Compendium `versions` link."""
        return resolve_link(self, "versions", typename=self.typename)


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
        return resolve_link(self, "draft", typename=self.typename)
