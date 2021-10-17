#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from pydash import py_

from typing import Dict


def is_draft(record_document: Dict):
    return not py_.get(record_document, "is_published", True)


def is_record(record_document: Dict):
    return not is_draft(record_document)


__all__ = (
    "is_draft",
    "is_record"
)
