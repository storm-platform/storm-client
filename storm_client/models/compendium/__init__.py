#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from .base import CompendiumBase
from .model import CompendiumDraft, CompendiumRecord

from .files import CompendiumFiles, CompendiumFileEntry, map_file_entry, create_file_object

__all__ = (
    "CompendiumBase",
    "CompendiumDraft",
    "CompendiumRecord",

    # Files
    "CompendiumFiles",
    "CompendiumFileEntry",

    # Helpers for files
    "map_file_entry",
    "create_file_object"
)