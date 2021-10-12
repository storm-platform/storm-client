#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from storm_client.models.node.base import NodeBase
from storm_client.models.node.encoder import NodeJSONEncoder
from storm_client.models.node.link import NodeDraftLink, NodeRecordLink


class NodeDraft(NodeBase):
    links_cls = NodeDraftLink
    serializer_cls = NodeJSONEncoder


class NodeRecord(NodeBase):
    links_cls = NodeRecordLink
    serializer_cls = NodeJSONEncoder


__all__ = (
    "NodeBase",
    "NodeDraft",
    "NodeRecord"
)
