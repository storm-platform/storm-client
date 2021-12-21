# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict

from typeguard import typechecked
from cachetools import LRUCache, cached

from .base import BaseService
from ..object_factory import ObjectFactory
from ..models.project import Project, ProjectList
from ..accessors.project import ProjectContextAccessor


@typechecked
class ProjectService(BaseService):
    """Research Project service."""

    base_path = "projects"
    """Base service path in the Rest API."""

    def __init__(self, url: str) -> None:
        super(ProjectService, self).__init__(url, self.base_path)

    @cached(cache=LRUCache(maxsize=128))
    def search(self, request_options: Dict = None, **kwargs) -> ProjectList:
        """Search for Research projects.

        Args:
            request_options (dict): Parameters to the ``httpx.Client.request`` method.

            **kwargs (dict): Search parameters.

        Returns:
            ProjectList: List with the founded Research Projects.
        """
        operation_result = self._create_request(
            "GET", self.url, params=kwargs, **request_options or {}
        )

        return ObjectFactory.resolve("ProjectList", operation_result.json())

    def create(self, project: Project, request_options: Dict = None) -> Project:
        """Create a new Research Project in the Storm WS.

        Args:
            project (Project): Project object to be created in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Created Research Project.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        operation_result = self._create_request(
            "POST", self.url, json=project, **request_options or {}
        )

        return ObjectFactory.resolve("Project", operation_result.json())

    def get(self, project_id: str, request_options: Dict = None) -> Project:
        """Get an existing Research Project from Storm WS.

        Args:
            project_id (str): Project ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Created Research Project.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        project_id_url = self._build_url(project_id)
        operation_result = self._create_request(
            "GET", project_id_url, **request_options or {}
        )

        return ObjectFactory.resolve("Project", operation_result.json())

    def save(self, project: Project, request_options: Dict = None) -> Project:
        """Update an existing Research Project in the Storm WS.

        Args:
            project (str): Project object to be saved in the Storm WS.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            Project: Updated Research Project.

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        project_id_url = self._build_url(project.id)
        operation_result = self._create_request(
            "PUT", project_id_url, json=project, **request_options or {}
        )

        return ObjectFactory.resolve("Project", operation_result.json())

    def delete(self, project_id, request_options: Dict = None):
        """Delete an existing Research Project from Storm WS.

        Args:
            project_id (str): Project ID.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            None

        See:
            For more details about ``http.Client.request`` options, please check
            the official documentation: https://www.python-httpx.org/api/#client
        """
        project_id_url = self._build_url(project_id)
        self._create_request("DELETE", project_id_url, **request_options or {})

    def __call__(self, project_id: str):
        """Call a project context."""
        return ProjectContextAccessor(self._build_url(project_id))
