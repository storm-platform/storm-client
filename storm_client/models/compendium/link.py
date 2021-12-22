# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField


class BaseCompendiumLink(BaseModel):
    """Base Compendium link class."""

    def __init__(self, data=None):
        super(BaseCompendiumLink, self).__init__(data or {})

    #
    # Data fields
    #

    files = LinkField("files", "CompendiumFiles")
    """Link to the Compendium files."""


class CompendiumRecordLink(BaseCompendiumLink):
    """Compendium Record (Published) link class."""

    #
    # Data fields
    #

    self = LinkField("files", "CompendiumRecord")
    """Link to the Compendium (Record) itself."""

    latest = LinkField("latest", "CompendiumRecord")
    """Link to the last version of the Compendium ."""

    versions = LinkField("versions", "CompendiumRecord")
    """Link to the Compendium versions index."""

    def __init__(self, data=None):
        super(CompendiumRecordLink, self).__init__(data or {})


class CompendiumDraftLink(BaseCompendiumLink):
    """Compendium Draft (Not published) link class."""

    #
    # Data fields
    #

    self = LinkField("draft", "CompendiumDraft")
    """Link to the Compendium (Draft) itself."""

    def __init__(self, data=None):
        super(CompendiumDraftLink, self).__init__(data or {})
