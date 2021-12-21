# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .base import BaseServiceContextAccessor
from .compendium import CompendiumContextAccessor


class ProjectContextAccessor(BaseServiceContextAccessor):
    """Research Project context accessor."""

    def __init__(self, url):
        super(ProjectContextAccessor, self).__init__(url)

    @property
    def compendium(self):
        """Compendium context accessor."""
        return CompendiumContextAccessor(self._url)
