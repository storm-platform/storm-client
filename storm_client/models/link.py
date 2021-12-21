# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from .base import BaseModel
from ..network import HTTPXClient
from ..object_factory import ObjectFactory


def resolve_link(model: BaseModel, field_path, typename, http_method="GET"):
    """Resolve a link into an available storm-client data class."""
    model.has_field(field_path)

    response = HTTPXClient.request(http_method, model.get_field(field_path)).json()
    if py_.has(response, "hits.hits"):  # for the `version` attribute
        return [
            ObjectFactory.resolve(typename, r) for r in py_.get(response, "hits.hits")
        ]

    return ObjectFactory.resolve(typename, response)
