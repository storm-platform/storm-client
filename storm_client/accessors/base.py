# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class BaseServiceContextAccessor:
    """Service context accessor base class.

    An ``Service context accessor`` is a simple class
    that makes access to a specific part of a web service.
    For example, when modeling a web service endpoint as a
    context accessor, we can access all objects, subendpoints,
    and actions through the defined accessor.

    In the case of the storm-client, we are using the context
    accessor to define endpoints like ``Project `` and ``Compendia``.
    So, all elements of these endpoints are made available through
    the accessor.
    """

    def __init__(self, url: str):
        """Initializer.

        Args:
            url (str): Base URL of the service endpoint that define the
            context accessor.
        """
        self._url = url
