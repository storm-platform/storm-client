# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from abc import ABC, abstractmethod


class JSONSerializable(ABC):
    @abstractmethod
    def to_json(self):
        ...


__all__ = "Serializer"
