# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_
from .model import Project, ProjectList


def init_model(factory):
    """Register the models in the object factory."""

    # defining the classes and name reference that will be
    # used in the object factory.
    factory_classes = [Project, ProjectList]

    # Register each class in the factory.
    py_.map(factory_classes, lambda cls: factory.register(cls.__name__, cls))


__all__ = (
    "Project",
    "ProjectList",
)
