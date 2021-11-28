# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
from collections import UserDict

from .base import CompendiumBase
from .files import map_file_entry


class CompendiumJSONEncoder(json.JSONEncoder):
    def default(self, o) -> dict:
        object_data = o
        if isinstance(o, UserDict):
            object_data = object_data.data

        if isinstance(o, CompendiumBase):
            map_file_entry(object_data, "metadata.execution.data.inputs")
            map_file_entry(object_data, "metadata.execution.data.outputs")
        return object_data  # generalized


__all__ = "CompendiumJSONEncoder"
