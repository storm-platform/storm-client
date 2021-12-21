# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pydash import py_

from typing import Dict, List
from typeguard import typechecked

from ...network import HTTPXClient
from ...services.base import BaseService
from ...models.compendium import CompendiumDraft


@typechecked
class CompendiumFileService(BaseService):
    """Execution Compendium Files service."""

    def __init__(self, url: str) -> None:
        super(CompendiumFileService, self).__init__(url)

    def define_files(
        self, compendium: CompendiumDraft, files: List, request_options: Dict = None
    ) -> CompendiumDraft:
        """Define which files will be uploaded to a Compendium Draft in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            files (list): A list with the filename to define.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Updated compendium draft.

        Note:
            In the ``user context`` only the compendia created by the user is
            available.
        """
        operation_url = compendium.get_field("links.files")

        # preparing the files
        files = py_.map(files, lambda x: {"key": os.path.join(x)})

        self._create_request("POST", operation_url, json=files, **request_options or {})
        return compendium

    def delete_defined_files(
        self, compendium: CompendiumDraft, files: List, request_options: Dict = None
    ):
        """Delete an already defined Compendium Draft files in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            files (list): A list with the filename to delete.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.
        """
        files_to_delete = compendium.links.files

        for file in files_to_delete.entries:
            if file.filename in files:
                self._create_request("DELETE", file.url, **request_options or {})

    def upload_files(
        self,
        compendium: CompendiumDraft,
        files: Dict,
        define_files: bool = True,
        commit_files: bool = True,
        request_options: Dict = None,
    ) -> CompendiumDraft:
        """Upload file content to the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            files (list): A list with the filename to delete.

            define_files (bool): Flag indicating that the files must be defined in the Storm WS.

            commit_files (bool): Flag indicating that the files uploaded must be committed also.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Updated compendium draft.
        """
        if define_files:
            compendium = self.define_files(
                compendium, list(files.keys()), request_options
            )

        responses = {}
        compendium_files = compendium.links.files

        for file in compendium_files.entries:

            # selecting the file to upload
            file_to_upload = files.get(file.filename)

            # uploading
            response = HTTPXClient.upload("PUT", file.content_url, file_to_upload)
            responses[file.filename] = response.status_code

            if commit_files:
                response_json = response.json()

                commit_url = py_.get(response_json, "links.commit")
                self._create_request("POST", commit_url, **request_options or {})
        return compendium
