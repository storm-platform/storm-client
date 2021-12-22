# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class IDExtractor:
    """ID Extractor.

    Class to centralize the definition of
    rules that should be applied in the
    Storm Client data classes objects to
    extract their ID in the Storm WS.
    """

    rules = {
        # identity function: when object is a
        # string, is assumed that the content
        # is a valid Storm WS id.
        "str": lambda x: x,
        "Deposit": lambda x: x.id,
        "Project": lambda x: x.id,
        "Pipeline": lambda x: x.id,
        "CompendiumRecord": lambda x: x.id,
        "DepositPluginService": lambda x: x.id,
    }

    @classmethod
    def extract(cls, obj):
        return cls.rules.get(obj.__class__.__name__).__call__(obj)
