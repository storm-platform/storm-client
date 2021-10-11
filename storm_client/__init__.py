#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""SpatioTemporal Open Research Manager."""
from .storm import Storm

from .models.node import NodeDraft, NodeRecord, NodeFiles
from .models.project import Project

from .version import __version__

#
# Configuring Object Factories
#
from .object_factory import ObjectFactory

ObjectFactory.register("Project", Project)
ObjectFactory.register("NodeDraft", NodeDraft)
ObjectFactory.register("NodeFiles", NodeFiles)
ObjectFactory.register("NodeRecord", NodeRecord)

__all__ = (
    "Storm",

    "__version__"
)
