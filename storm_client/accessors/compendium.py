# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .base import BaseServiceContextAccessor
from ..services.compendium import (
    CompendiumRecordService,
    CompendiumDraftService,
    CompendiumFileService,
    CompendiumSearchService,
)


class CompendiumContextAccessor(BaseServiceContextAccessor):
    """Compendium context accessor."""

    def __init__(self, url):
        super(CompendiumContextAccessor, self).__init__(url)

    @property
    def draft(self):
        """Compendium draft service."""
        return CompendiumDraftService(self._url)

    @property
    def record(self):
        """Compendium record service."""
        return CompendiumRecordService(self._url)

    @property
    def files(self):
        """Compendium file service."""
        return CompendiumFileService(self._url)

    @property
    def search(self):
        """Compendium search service."""
        return CompendiumSearchService(self._url)
