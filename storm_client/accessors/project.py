# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .base import BaseServiceContextAccessor
from .compendium import CompendiumContextAccessor

from ..services.job import JobService
from ..services.deposit import DepositService
from ..services.pipeline import PipelineService


class ProjectContextAccessor(BaseServiceContextAccessor):
    """Research Project context accessor."""

    def __init__(self, url):
        super(ProjectContextAccessor, self).__init__(url)

    @property
    def compendium(self):
        """Compendium context accessor."""
        return CompendiumContextAccessor(self._url)

    @property
    def pipeline(self):
        """Pipeline context accessor."""
        return PipelineService(self._url)

    @property
    def deposit(self):
        """Deposit context accessor."""
        return DepositService(self._url)

    @property
    def job(self):
        """Job context accessor."""
        return JobService(self._url)
