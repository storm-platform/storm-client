# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .model import Project, ProjectList
from ..factory import init_model_factory


def init_model(factory):
    """Register the models in the object factory."""
    init_model_factory(factory, [Project, ProjectList])


__all__ = (
    "Project",
    "ProjectList",
)
