#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
from storm_client.services.base import BaseService
from storm_client.object_factory import ObjectFactory


class ProjectService(BaseService):

    def __init__(self, url: str, access_token: str) -> None:
        base_path = "project"
        super(ProjectService, self).__init__(url, base_path, access_token)

    def search(self, **kwargs):
        operation_result = self._create_request("GET", self.url, **kwargs)

        return [
            ObjectFactory.resolve("Project", response) for response in operation_result.json()
        ]

    def create(self, json, **kwargs):
        operation_result = self._create_request("POST", self.url, json=json, **kwargs)

        return ObjectFactory.resolve("Project", operation_result.json())

    def delete(self, project_id, **kwargs):
        project_id_url = self._build_url([str(project_id)])

        return self._create_request("DELETE", project_id_url, **kwargs).json()

    def resolve(self, project_id, **kwargs):
        project_id_url = self._build_url([str(project_id)])
        project_object = self._create_request("GET", project_id_url, **kwargs).json()

        return ObjectFactory.resolve("Project", project_object)


__all__ = (
    "ProjectService"
)
