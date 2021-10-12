#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from abc import ABC, abstractmethod


class Serializer(ABC):

    @abstractmethod
    def to_json(self): ...


__all__ = (
    "Serializer"
)
