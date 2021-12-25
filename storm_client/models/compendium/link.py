# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from ..base import BaseModel
from ...field import LinkField, DictField


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

    self = LinkField("self", "CompendiumRecord")
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

    self = LinkField("self", "CompendiumDraft")
    """Link to the Compendium (Draft) itself."""

    def __init__(self, data=None):
        super(CompendiumDraftLink, self).__init__(data or {})


class CompendiumFileLink(BaseModel):
    """Compendium Files link class."""

    def __init__(self, data=None):
        super(CompendiumFileLink, self).__init__(data or {})

    #
    # Data fields
    #

    self = DictField("self")
    """Link to the Compendium file itself."""

    content = DictField("content")
    """Link to the Compendium (Record) files content."""

    commit = DictField("commit")
    """Link to Commit a Compendium file."""
