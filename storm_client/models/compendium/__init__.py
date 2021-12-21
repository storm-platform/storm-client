# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .base import CompendiumBase
from .link import CompendiumDraftLink, CompendiumRecordLink
from .model import CompendiumDraft, CompendiumRecord, CompendiumRecordList

from .files import (
    CompendiumFiles,
    CompendiumFileMetadata,
)

from .descriptor import ExecutionDescriptor
from ..factory import init_model_factory


def init_model(factory):
    """Register the models in the object factory."""

    # defining the classes and name reference that will be
    # used in the object factory.
    factory_classes = [
        CompendiumDraft,
        CompendiumFiles,
        CompendiumRecord,
        CompendiumDraftLink,
        CompendiumRecordLink,
        CompendiumRecordList,
        CompendiumFileMetadata,
    ]

    init_model_factory(factory, factory_classes)


__all__ = (
    # Compendia
    "CompendiumBase",
    "CompendiumDraft",
    "CompendiumRecord",
    "CompendiumRecordList",
    # Files
    "CompendiumFiles",
    "CompendiumFileMetadata",
    # Execution descriptors
    "ExecutionDescriptor",
)
