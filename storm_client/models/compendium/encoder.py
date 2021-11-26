# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json

from .base import CompendiumBase
from .files import map_file_entry


class CompendiumJSONEncoder(json.JSONEncoder):
    def default(self, o) -> dict:
        if isinstance(o, CompendiumBase):
            object_data = o.data

            map_file_entry(object_data, "data.inputs")
            map_file_entry(object_data, "data.outputs")

            return object_data

        raise TypeError("`CompendiumJSONEncoder` only encode `CompendiumBase` objects.")


__all__ = "CompendiumJSONEncoder"
