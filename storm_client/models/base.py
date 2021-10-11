#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from pydash import py_

from collections import UserDict


class BaseModel(UserDict):

    def _default_value(self, property_path, value):
        return py_.defaults_deep(self, py_.set_({}, property_path, value))


__all__ = (
    "BaseModel"
)
