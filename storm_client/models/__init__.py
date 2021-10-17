#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from pydash import py_

from ..object_factory import ObjectFactory

from ..models.project import Project
from .node.files import NodeFiles, NodeFileEntry
from .node.link import NodeDraftLink, NodeRecordLink
from .node.model import NodeDraft, NodeRecord, NodeRecordList

FACTORY_CLASSES = {
    "Project": Project,
    "NodeDraft": NodeDraft,
    "NodeFiles": NodeFiles,
    "NodeRecord": NodeRecord,
    "NodeFileEntry": NodeFileEntry,
    "NodeDraftLink": NodeDraftLink,
    "NodeRecordLink": NodeRecordLink,
    "NodeRecordList": NodeRecordList
}

py_.map(
    FACTORY_CLASSES.keys(),
    lambda x: ObjectFactory.register(x, FACTORY_CLASSES[x])
)

__all__ = (
    "FACTORY_CLASSES"
)
