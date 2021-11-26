# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from collections import UserDict

from .serializer import JSONSerializable


class BaseModel(UserDict, JSONSerializable):
    def _default_value(self, property_path, value):
        return py_.defaults_deep(self, py_.set_({}, property_path, value))


__all__ = "BaseModel"
