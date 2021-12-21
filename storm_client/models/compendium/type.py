# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from typing import Dict


def is_draft(record_document: Dict):
    """Check if the document is a draft (Not published)."""
    return not py_.get(record_document, "is_published", True)


def is_record(record_document: Dict):
    """Check if the document is a record (Published)."""
    return not is_draft(record_document)
