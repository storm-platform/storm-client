# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from abc import ABC
from pydash import py_

from collections import UserDict


class BaseModel(UserDict, ABC):
    """Base class for the storm-client data models."""

    def _set_default_value(self, property_path, value):
        """Define default values in the ``UserDict.data`` attribute."""
        return py_.defaults_deep(self.data, py_.set_({}, property_path, value))

    def get_field(self, data_field: str, default=None):
        """Access data field from the object data document."""
        return py_.get(self.data, data_field, default)

    def has_field(self, field: str):
        """Check if a property exists."""
        if not py_.has(self.data, field):
            raise AttributeError(f"{field} attribute not available for this object!")

    def for_json(self):  # ``simplejson`` encoder method
        """Encode the object into a dict-like serializable object."""
        return self.data
