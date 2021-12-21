# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_
from typing import List


def init_model_factory(factory: "ObjectFactory", classes: List[object]):
    """Helper function to register the classes
    in the Object Factory.

    Args:
        factory (ObjectFactory): Object Factory class

        classes (List[object]): Classes to be registered in the Object Factory.
    """

    # Register each class in the factory.
    py_.map(classes, lambda cls: factory.register(cls.__name__, cls))
