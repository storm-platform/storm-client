

import os

from urllib.parse import urljoin
from storm_client.services.base import BaseService
from storm_client.object_factory import ObjectFactory


class ProjectService(BaseService):

    def __init__(self, url: str, access_token: str) -> None:
        super(ProjectService, self).__init__(url, access_token)
        self._operation_url = self._build_url("project")

    def search(self, **kwargs):
        operation_result = self._create_request(
            "GET", self._operation_url, **kwargs)

        return [
            ObjectFactory.resolve("Project", response) for response in operation_result.json()
        ]

    def create(self, json, **kwargs):
        operation_result = self._create_request(
            "POST", self._operation_url, json=json, **kwargs)

        return ObjectFactory.resolve("Project", operation_result.json())

    def delete(self, project_id, **kwargs):
        project_id_url = urljoin(self._operation_url, str(project_id))

        return self._create_request(
            "DELETE", project_id_url, **kwargs).json()

    def resolve(self, project_id, **kwargs):
        project_id_url = urljoin(self._build_url("project/"), str(project_id))

        project_object = self._create_request(
            "GET", project_id_url, **kwargs).json()

        return ObjectFactory.resolve("Project", project_object)
