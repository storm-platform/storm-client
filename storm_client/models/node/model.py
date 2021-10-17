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

from .base import NodeBase
from .type import is_draft
from .encoder import NodeJSONEncoder
from .link import NodeDraftLink, NodeRecordLink


class NodeDraft(NodeBase):
    links_cls = NodeDraftLink
    serializer_cls = NodeJSONEncoder


class NodeRecord(NodeBase):
    links_cls = NodeRecordLink
    serializer_cls = NodeJSONEncoder


#
# Record Collection
#
class NodeRecordList(UserList):
    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError('The `data` argument must be a valid sequence type.')

        data = py_.map(data, lambda obj: NodeDraft(obj) if is_draft(obj) else NodeRecord(obj))
        super(NodeRecordList, self).__init__(data)


__all__ = (
    "NodeDraft",
    "NodeRecord",
    "NodeRecordList"
)
