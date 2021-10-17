#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import json

from .base import NodeBase
from .files import map_file_entry


class NodeJSONEncoder(json.JSONEncoder):

    def default(self, o) -> dict:
        if isinstance(o, NodeBase):
            object_data = o.data

            map_file_entry(object_data, "data.inputs")
            map_file_entry(object_data, "data.outputs")

            return object_data

        raise TypeError("`NodeJSONEncoder` only encode `NodeBase` objects.")


__all__ = (
    "NodeJSONEncoder"
)
