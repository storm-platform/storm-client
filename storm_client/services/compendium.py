# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import asyncio
import posixpath

import warnings

from pydash import py_

from typeguard import typechecked
from typing import Dict, List, Union

from .base import BaseService
from ..models import CompendiumRecord

from ..network import HTTPXClient
from ..object_factory import ObjectFactory

from ..models.compendium import CompendiumDraft, CompendiumBase, create_file_object


def _node_obj_to_dict(node_obj: Union[Dict, CompendiumBase]):
    """Transform CompendiumBase instance to a dict instance."""
    return node_obj.to_json() if isinstance(node_obj, CompendiumBase) else node_obj


@typechecked
class CompendiumService(BaseService):
    def __init__(
        self, url: str, access_token: str, project_id: str, as_draft: bool = False
    ) -> None:
        base_path = posixpath.join("projects", str(project_id), "compendia")
        super(CompendiumService, self).__init__(url, base_path, access_token)

        self._as_draft = as_draft
        self._project_id = project_id

        # defining the node type
        self._node_type = "CompendiumRecord"
        self._complement_url = ""

        if as_draft:
            self._node_type = "CompendiumDraft"
            self._complement_url = "draft"

    @property
    def is_draft_service(self):
        return self._as_draft

    def resolve(
        self, node_id: str, request_options: Dict = {}
    ) -> Union[CompendiumBase, None]:
        node_id_url = self._build_url([node_id, self._complement_url])
        operation_result = self._create_request("GET", node_id_url, **request_options)

        return ObjectFactory.resolve(self._node_type, operation_result.json())

    def create(self, data: CompendiumDraft, request_options: Dict = {}):
        json = _node_obj_to_dict(data)
        operation_result = self._create_request(
            "POST", self.url, json=json, **request_options
        )

        return ObjectFactory.resolve(self._node_type, operation_result.json())

    def save(self, data: CompendiumDraft, request_options: Dict = {}):
        json = _node_obj_to_dict(data)

        self_node_link = py_.get(json, "links.self", None)
        operation_result = self._create_request(
            "PUT", self_node_link, json=json, **request_options
        )

        # Editable records on storm are new drafts
        return ObjectFactory.resolve("CompendiumDraft", operation_result.json())

    def new_version(
        self, data: CompendiumRecord, request_options: Dict = {}
    ) -> CompendiumDraft:
        json = _node_obj_to_dict(data)

        versions_link = py_.get(json, "links.versions", None)
        operation_result = self._create_request(
            "POST", versions_link, json=json, **request_options
        )

        # New records on storm are drafts
        return ObjectFactory.resolve("CompendiumDraft", operation_result.json())

    def publish(
        self, data: CompendiumDraft, request_options: Dict = {}
    ) -> CompendiumRecord:
        # publishing the resource
        publish_node = data.links["publish"]

        response = self._create_request("POST", publish_node, **request_options)
        return ObjectFactory.resolve(
            "CompendiumRecord", response.json()
        )  # record is fixed here


@typechecked
class CompendiumFilesService(BaseService):
    def __init__(
        self, url: str, access_token: str, node_resource: CompendiumDraft
    ) -> None:
        super(CompendiumFilesService, self).__init__(url, access_token=access_token)

        if py_.is_none(node_resource.id):
            raise TypeError(
                "The `node_resource` should be a defined Storm Service object."
            )

        self._node_resource = node_resource
        self._node_link_type = type(node_resource.links).__name__

    def _define_node_files(self, files: List, request_options: Dict = {}) -> Dict:
        # preparing the files
        files = py_.map(files, create_file_object)
        files_link = py_.get(self._node_resource, "links.files", None)

        operation_result = self._create_request(
            "POST", files_link, json=files, **request_options
        )
        return operation_result.json()

    def upload_files(
        self, files: Dict, commit: bool = False, request_options: Dict = {}
    ) -> CompendiumDraft:
        # extracting files
        get_file_entry = lambda obj: py_.map(obj, lambda x: x["key"])
        node_resource_files = py_.interleave(
            get_file_entry(self._node_resource.inputs),
            get_file_entry(self._node_resource.outputs),
        )

        # checking if files is defined on record (to avoid API validation errors)
        intersected_files = py_.intersection(node_resource_files, files.keys())

        # checking for invalid files
        invalid_files = py_.difference(node_resource_files, files.keys())
        invalid_files = ",".join(invalid_files)

        responses = []
        if intersected_files:
            if invalid_files:
                warnings.warn(
                    f"Invalid files found ({invalid_files}). Only files defined on Node will be uploaded."
                )

            defined_files = self._define_node_files(intersected_files)

            for defined_file in py_.get(defined_files, "entries", []):
                defined_file_key = defined_file["key"]
                defined_file_content_link = py_.get(defined_file, "links.content")

                # uploading the file
                file_to_upload = files.get(defined_file_key)

                response = asyncio.run(
                    HTTPXClient.upload("PUT", defined_file_content_link, file_to_upload)
                )
                responses.append(response)

                if commit:
                    response_json = response.json()

                    commit_url = py_.get(response_json, "links.commit")
                    self._create_request(
                        "POST", commit_url, json=files, **request_options
                    )

            return self._node_resource.links.self

        # error if only invalid files is defined in input.
        if invalid_files:
            raise ValueError(
                f"Invalid files found ({invalid_files}). "
                f"Files must be defined in the Node node before being sent to the server"
            )


__all__ = ("CompendiumService", "CompendiumFilesService")
