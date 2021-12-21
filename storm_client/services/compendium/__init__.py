# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .base import BaseCompendiumService

from .compendium import (
    BaseCompendiumHandlerService,
    CompendiumRecordService,
    CompendiumDraftService,
)

from .files import CompendiumFileService
from .search import CompendiumSearchService

__all__ = (
    "BaseCompendiumService",
    # Compendium (itself) service
    "BaseCompendiumHandlerService",
    "CompendiumDraftService",
    "CompendiumRecordService",
    # File service
    "CompendiumFileService",
    # Search service
    "CompendiumSearchService",
)
