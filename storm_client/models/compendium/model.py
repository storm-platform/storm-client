#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from pydash import py_

from typing import Sequence
from collections import UserList

from .base import CompendiumBase
from .type import is_draft
from .encoder import CompendiumJSONEncoder
from .link import CompendiumDraftLink, CompendiumRecordLink


class CompendiumDraft(CompendiumBase):
    links_cls = CompendiumDraftLink
    serializer_cls = CompendiumJSONEncoder


class CompendiumRecord(CompendiumBase):
    links_cls = CompendiumRecordLink
    serializer_cls = CompendiumJSONEncoder


#
# Record Collection
#
class CompendiumRecordList(UserList):
    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError('The `data` argument must be a valid sequence type.')

        data = py_.map(data, lambda obj: CompendiumDraft(obj) if is_draft(obj) else CompendiumRecord(obj))
        super(CompendiumRecordList, self).__init__(data)


__all__ = (
    "CompendiumDraft",
    "CompendiumRecord",
    "CompendiumRecordList"
)
