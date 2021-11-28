# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from typing import Sequence
from collections import UserList

from .type import is_draft
from .encoder import CompendiumJSONEncoder

from .base import CompendiumBase
from .descriptor import ExecutionDescriptor

from .link import CompendiumDraftLink, CompendiumRecordLink


class CompendiumDraft(CompendiumBase):
    links_cls = CompendiumDraftLink
    serializer_cls = CompendiumJSONEncoder
    descriptor_cls = ExecutionDescriptor


class CompendiumRecord(CompendiumBase):
    links_cls = CompendiumRecordLink
    serializer_cls = CompendiumJSONEncoder
    descriptor_cls = ExecutionDescriptor


#
# Record Collection
#
class CompendiumRecordList(UserList):
    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError("The `data` argument must be a valid sequence type.")

        data = py_.map(
            data,
            lambda obj: CompendiumDraft(obj)
            if is_draft(obj)
            else CompendiumRecord(obj),
        )
        super(CompendiumRecordList, self).__init__(data)


__all__ = ("CompendiumDraft", "CompendiumRecord", "CompendiumRecordList")
