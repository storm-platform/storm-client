# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class TokenStore:
    """Single source of truth for access token storage."""

    _access_token = None

    @classmethod
    def save_token(cls, token):
        """Save a token."""
        cls._access_token = token

    @classmethod
    def get_token(cls):
        """Get a token."""
        if not cls._access_token:
            raise RuntimeError("Access token is not defined yet. Please, define it.")
        return cls._access_token
