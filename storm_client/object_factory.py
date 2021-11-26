# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""SpatioTemporal Open Research Manager object factory."""


class ObjectFactory:
    _factories = {}

    @classmethod
    def register(cls, name, factory):
        cls._factories[name] = factory

    @classmethod
    def exists(cls, name):
        return name in cls._factories

    @classmethod
    def resolve(cls, datatype, data):
        if cls.exists(datatype):
            return cls._factories[datatype](data)
        raise NotImplemented(f"Factory for {datatype} is not implemented.")


__all__ = "ObjectFactory"
