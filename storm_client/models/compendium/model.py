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
from .descriptor import ExecutionDescriptor

from .link import CompendiumDraftLink, CompendiumRecordLink


class CompendiumDraft(CompendiumBase):
    """Compendium draft.

    In the Storm WS, a ``Draft`` is a record in the service
    that is not published for other users. So, you should use
    this class to handle compendium objects that are not finished
    or have work in progress.
    """

    links_cls = CompendiumDraftLink
    descriptor_cls = ExecutionDescriptor

    @property
    def errors(self):
        """Compendium errors."""
        return self.get_field("errors")

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

    links_cls = CompendiumRecordLink
    descriptor_cls = ExecutionDescriptor


class CompendiumRecordList(UserList):
    """A collection of Compendia (Draft and Records)."""

    def __init__(self, data=None):
        if not isinstance(data, (list, tuple)):
            raise ValueError(
                "The CompendiumRecordList `data` argument must be a valid ``tuple`` or ``list``."
            )

        data = py_.map(
            data,
            lambda obj: CompendiumDraft(obj)
            if is_draft(obj)
            else CompendiumRecord(obj),
        )
        super(CompendiumRecordList, self).__init__(data)
