# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from collections import UserList

from .type import is_draft
from .base import CompendiumBase

from ...field import ObjectField, DictField


class CompendiumDraft(CompendiumBase):
    """Compendium draft.

    In the Storm WS, a ``Draft`` is a record in the service
    that is not published for other users. So, you should use
    this class to handle compendium objects that are not finished
    or have work in progress.
    """

    #
    # Data fields
    #

    errors = DictField("errors", [])
    """Compendium draft errors (in the submitted document)."""

    links = ObjectField("links", "CompendiumDraftLink")
    """Compendium draft links."""

    @property
    def has_errors(self):
        """Flag indicating if the compendium draft document has errors.."""
        return self.errors is not None


class CompendiumRecord(CompendiumBase):
    """Compendium record.

    In the Storm WS, a ``Record`` is a already finished and published
    record, available for all users in a project. You can create
    ``Record`` from ``Draft`` publishing the ``Draft``. Once create,
    a ``Record`` can't be deleted or replaced.
    """

    #
    # Data fields
    #

    links = ObjectField("links", "CompendiumRecordLink")
    """Compendium record links."""


class CompendiumRecordList(UserList):
    """A collection of Compendia (Draft and Records)."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        super(CompendiumRecordList, self).__init__(
            py_.map(
                data,
                lambda obj: CompendiumDraft(obj)
                if is_draft(obj)
                else CompendiumRecord(obj),
            )
        )
