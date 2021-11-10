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
from .compendium.files import CompendiumFiles, CompendiumFileEntry
from .compendium.link import CompendiumDraftLink, CompendiumRecordLink
from .compendium.model import CompendiumDraft, CompendiumRecord, CompendiumRecordList

FACTORY_CLASSES = {
    "Project": Project,
    "CompendiumDraft": CompendiumDraft,
    "CompendiumFiles": CompendiumFiles,
    "CompendiumRecord": CompendiumRecord,
    "CompendiumFileEntry": CompendiumFileEntry,
    "CompendiumDraftLink": CompendiumDraftLink,
    "CompendiumRecordLink": CompendiumRecordLink,
    "CompendiumRecordList": CompendiumRecordList
}

py_.map(
    FACTORY_CLASSES.keys(),
    lambda x: ObjectFactory.register(x, FACTORY_CLASSES[x])
)

__all__ = (
    "FACTORY_CLASSES"
)
