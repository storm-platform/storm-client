# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import difflib

from pydash import py_
from collections import UserList

from ...field import DictField, ObjectField
from ..base import VersionedModel
from ..extractor import IDExtractor


class Pipeline(VersionedModel):
    """Pipeline model.

    A pipeline is an ordered sequence of steps representing the processing
    flow applied in research to produce the results. In the Storm WS, the
    pipeline is modeled as a  Directed Acyclic Graph (DAG), where each step
    is a Record Compendium (Published in the project).
    """

    #
    # Data fields
    #

    # General informations.
    is_finished = DictField("is_finished")
    """Flag indicating if the pipeline is finished."""

    # Metadata.
    metadata = DictField("metadata")
    """Complete pipeline metadata."""

    title = DictField("metadata.title")
    """Pipeline title (From metadata)."""

    description = DictField("metadata.description")
    """Pipeline description (From metadata)."""

    version = DictField("metadata.version")
    """Pipeline version (From metadata)."""

    # Compendium graph data.
    graph = DictField("metadata.graph")
    """Pipeline graph."""

    # Links
    links = ObjectField("links", "PipelineLink")
    """Compendium draft links."""

    @property
    def compendia(self):
        """Pipeline compendia."""
        return self._current_state

    @compendia.setter
    def compendia(self, compendia):
        self._current_state = compendia

    def __init__(self, data=None, **kwargs):
        super(Pipeline, self).__init__(data or kwargs or {})

        # saving the original state of the
        # compendia available in the graph.
        self._original_state = list(self.get_field("graph.nodes", {}).keys())
        self._current_state = self._original_state.copy()

    def diff(self):
        """Generate a difference between the original
        state and the actual state."""
        added = []
        removed = []

        # before start, let's validate the types:
        compendia_types = (
            py_.chain([self._current_state, self._original_state])
            .flatten()
            .map(lambda x: x.__class__.__name__)
            .filter(lambda x: x not in IDExtractor.rules)
            .value()
        )
        if compendia_types:
            raise TypeError(
                "Invalid Compendia! You can only define a pipeline compendia using ``str`` and ``CompendiumRecord``"
            )

        # handle the available objects.
        _current_state = py_.map(self._current_state, IDExtractor.extract)
        _original_state = py_.map(self._original_state, IDExtractor.extract)

        # matcher
        matcher = difflib.SequenceMatcher(None, _original_state, _current_state)

        # getting the difference
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            # states
            current_value_state = _current_state[j1:j2]
            original_value_state = _original_state[i1:i2]

            # processing the changes
            if tag == "equal":
                continue

            elif tag == "replace":
                # checking if the replaced value
                # was already defined in the list before.
                if current_value_state in _original_state:
                    continue

                # following the documentation:
                # 'replace':  a[i1:i2] should be replaced by b[j1:j2]
                added.extend(current_value_state)
                removed.extend(original_value_state)

            elif tag == "delete":
                removed.extend(original_value_state)

            else:
                added.extend(current_value_state)
        return ("added", added), ("removed", removed)


class PipelineList(UserList):
    """A collection of Research pipelines."""

    def __init__(self, data=None):
        if py_.has(data, "hits.hits"):
            data = py_.get(data, "hits.hits")

        super(PipelineList, self).__init__(py_.map(data, lambda obj: Pipeline(obj)))
