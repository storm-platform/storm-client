# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import difflib

from pydash import py_
from collections import UserList

from ..base import VersionedModel
from ..compendium import CompendiumRecord


class Pipeline(VersionedModel):
    """Pipeline model.

    A pipeline is an ordered sequence of steps representing the processing
    flow applied in research to produce the results. In the Storm WS, the
    pipeline is modeled as a  Directed Acyclic Graph (DAG), where each step
    is a Record Compendium (Published in the project).
    """

    def __init__(self, data=None, **kwargs):
        super(Pipeline, self).__init__(data or kwargs or {})

        # saving the original state of the
        # compendia available in the graph.
        self._original_state = list(self.get_field("graph.nodes", {}).keys())
        self._current_state = self._original_state.copy()

    @property
    def id(self):
        """Pipeline ID."""
        return self.get_field("id")

    @property
    def is_finished(self):
        """Pipeline ID."""
        return self.get_field("is_finished")

    @property
    def title(self):
        """Pipeline title."""
        return self.get_field("metadata.title")

    @property
    def description(self):
        """Pipeline description."""
        return self.get_field("metadata.description")

    @property
    def version(self):
        """Pipeline version."""
        return self.get_field("metadata.version")

    @property
    def compendia(self):
        """Pipeline compendia."""
        return self._current_state

    @compendia.setter
    def compendia(self, compendia):
        self._current_state = compendia

    @property
    def metadata(self):
        """Pipeline full metadata."""
        return self.get_field("metadata")

    @property
    def graph(self):
        """Pipeline graph."""
        return self.get_field("graph")

    def diff(self):
        """Generate a difference between the original
        state and the actual state."""
        added = []
        removed = []

        # mutation: before start, we will transform all
        # compendia values in valid string ``id``.
        extractors = {
            str: lambda x: x,
            CompendiumRecord: lambda x: x.id,
        }

        # before start, let's validate the types:
        compendia_types = (
            py_.chain([self._current_state, self._original_state])
            .flatten()
            .map(lambda x: type(x))
            .filter(lambda x: x not in extractors)
            .value()
        )
        if compendia_types:
            raise TypeError(
                "Invalid Compendia! You can only define a pipeline compendia using ``str`` and ``CompendiumRecord``"
            )

        # now, we can handle the states
        _current_state = py_.map(
            self._current_state, lambda x: extractors.get(type(x))(x)
        )
        _original_state = py_.map(
            self._original_state, lambda x: extractors.get(type(x))(x)
        )

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
        # fixme: this is in the wrong place.
        if py_.has(data, "hits.hits"):  # elasticsearch specific result format
            data = py_.get(data, "hits.hits")

        if not isinstance(data, (list, tuple)):
            raise ValueError(
                "The `data` argument must be a valid ``list`` or ``tuple`` type."
            )

        data = py_.map(data, lambda obj: Pipeline(obj))
        super(PipelineList, self).__init__(data)
