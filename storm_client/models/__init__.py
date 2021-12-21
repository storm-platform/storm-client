# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from importlib import import_module
from ..object_factory import ObjectFactory

DATA_MODELS = [
    "storm_client.models.project",
    "storm_client.models.compendium",
]

# initializing the models
for module in DATA_MODELS:
    mod = import_module(module)
    mod.init_model(ObjectFactory)
