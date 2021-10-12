#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import json
import os

from pydash import py_

from storm_client.models.node.base import NodeBase


class NodeJSONEncoder(json.JSONEncoder):

    def _create_file_key(self, filename):
        if isinstance(filename, str):
            return {"key": os.path.join(filename)}
        return filename

    def default(self, o) -> dict:
        if isinstance(o, NodeBase):
            object_data = o.data

            # applying rules to convert files
            set_inputs = lambda data, prop: py_.set(data, prop,
                                                    py_.chain(data).get(prop).map(
                                                        self._create_file_key).value())

            set_inputs(object_data, "data.inputs")
            set_inputs(object_data, "data.outputs")

            return object_data

        raise TypeError("NodeJSONEncoder only encode `NodeBase` objects.")


__all__ = (
    "NodeJSONEncoder"
)
