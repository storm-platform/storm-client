# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict, Union

from typeguard import typechecked
from cachetools import LRUCache, cached

from .base import RecordOperatorService
from ..models.extractor import IDExtractor
from ..models.project import Project, ProjectList
from ..accessors.project import ProjectContextAccessor


@typechecked
class ProjectService(RecordOperatorService):
    """Research Project service."""

    base_path = "projects"
    """Base service path in the Rest API."""

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> ProjectList:
        """Search for Research projects.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            ProjectList: List with the founded Research Projects.
        """
        return self._create_op_search("ProjectList", request_options, **kwargs)

    def create(self, project: Project, request_options: Dict = None) -> Project:
        """Create a new Research Project in the Storm WS.

        Args:
            project (Project): Project object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Created Research Project.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_create(project, "Project", request_options)

    def get(
        self, project: Union[str, Project], request_options: Dict = None
    ) -> Project:
        """Get an existing Research Project from Storm WS.

        Args:
            project (Union[str, Project]): Project ID or Project object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Research Project object.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_get(
            IDExtractor.extract(project), "Project", request_options
        )

    def save(self, project: Project, request_options: Dict = None) -> Project:
        """Update an existing Research Project in the Storm WS.

        Args:
            project (Project): Project object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Updated Research Project.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_save(project, "Project", request_options)

    def delete(self, project: Union[str, Project], request_options: Dict = None):
        """Delete an existing Research Project in the Storm WS.

        Args:
            project (Union[str, Project]): Project ID or Project object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        return self._create_op_delete(IDExtractor.extract(project), request_options)

    def finalize(self, project: Union[str, Project], request_options: Dict = None):
        """Finalize an existing Research Project in the Storm WS.

        Args:
            project (Union[str, Project]): Project ID or Project object.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Updated Research Project.

        See:
            For more details about ``httpx.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        self._create_op_action(
            IDExtractor.extract(project), "actions/finish", "POST", request_options
        )

        return self.get(project)

    def __call__(self, project: Union[str, Project]):
        """Call a project context."""
        return ProjectContextAccessor(self._build_url(IDExtractor.extract(project)))
