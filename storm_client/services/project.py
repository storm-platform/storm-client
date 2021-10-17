#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from typing import Dict
from typeguard import typechecked

from .base import BaseService
from ..object_factory import ObjectFactory
from ..models.project import Project, ProjectList


@typechecked
class ProjectService(BaseService):

    def __init__(self, url: str, access_token: str) -> None:
        base_path = "project"
        super(ProjectService, self).__init__(url, base_path, access_token)

    def search(self, request_options: Dict = {}, **kwargs) -> ProjectList:
        operation_result = self._create_request("GET", self.url, params=kwargs, **request_options)

        return ProjectList(operation_result.json())

    def create(self, data: Project, request_options: Dict = {}) -> Project:
        json = data.to_json()
        operation_result = self._create_request("POST", self.url, json=json, **request_options)

        return ObjectFactory.resolve("Project", operation_result.json())

    def delete(self, project_id, request_options: Dict = {}) -> Dict:
        project_id_url = self._build_url([str(project_id)])

        return self._create_request("DELETE", project_id_url, **request_options).json()

    def resolve(self, project_id: int, request_options: Dict = {}) -> Project:
        project_id_url = self._build_url([str(project_id)])
        project_object = self._create_request("GET", project_id_url, **request_options).json()

        return ObjectFactory.resolve("Project", project_object)


__all__ = (
    "ProjectService"
)
