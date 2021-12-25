# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pathlib import Path

import asyncio
from pydash import py_

from typing import Dict, List, Union
from typeguard import typechecked

from ...network import HTTPXClient
from .base import BaseCompendiumService
from ...models.compendium import CompendiumBase, CompendiumDraft


@typechecked
class CompendiumFileService(BaseCompendiumService):
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
        return compendium.links.self

    def delete_defined_files(
        self, compendium: CompendiumDraft, files: List, request_options: Dict = None
    ):
        """Delete already defined Compendium Draft files in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            files (list): A list with the filename to delete.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Updated compendium draft.
        """
        files_to_delete = compendium.links.files

        for file in files_to_delete.entries:
            if file.filename in files:
                self._create_request("DELETE", file.url, **request_options or {})

        return compendium.links.self

    def commit_defined_files(
        self, compendium: CompendiumDraft, files: List, request_options: Dict = None
    ):
        """Commit already defined Compendium Draft files in the Storm WS.

        Args:
            compendium (CompendiumDraft): Compendium Draft object.

            files (list): A list with the filename to delete.

            request_options (dict): Parameters to the ``httpx.Client.request`` method.

        Returns:
            CompendiumDraft: Updated compendium draft.
        """
        files_to_commit = compendium.links.files

        for file in files_to_commit.entries:
            if file.filename in files:
                self._create_request("POST", file.links.commit, **request_options or {})

        return compendium.links.self

    def upload_files(
        self,
        compendium: CompendiumDraft,
        files: Dict,
        define_files: bool = False,
        commit_files: bool = False,
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

        compendium_files = compendium.links.files
        for file in compendium_files.entries:

            # selecting the file to upload
            file_to_upload = files.get(file.filename)

            # uploading
            response = HTTPXClient.upload("PUT", file.links.content, file_to_upload)

            if commit_files:
                response_json = response.json()

                commit_url = py_.get(response_json, "links.commit")
                self._create_request("POST", commit_url, **request_options or {})
        return compendium.links.self  # reload from service

    async def _async_download_files(
        self,
        compendium: CompendiumBase,
        output_directory: Union[str, Path],
        files: List[str] = None,
        **kwargs
    ) -> Path:
        """Download compendium files from the Storm WS.

        Args:
            compendium (CompendiumBase): Compendium object.

            output_directory (Union[str, Path]):

            files (list): A list with the filename to delete.

            kwargs (dict): Extra parameters to the ``storm_client.models.compendium.files.CompendiumFiles.download``.

        Returns:
            Path: Path to the output directory.
        """
        output_directory = Path(output_directory)
        output_directory.mkdir(exist_ok=True)

        downloads = []
        for file in compendium.links.files.entries:
            if files and file.filename not in files:
                continue

            downloads.append(file.download(output_directory, **kwargs))
        await asyncio.gather(*downloads)

        return output_directory

    def download_files(
        self,
        compendium: CompendiumBase,
        output_directory: Union[str, Path],
        files: List[str] = None,
        **kwargs
    ) -> Path:
        """Download compendium files from the Storm WS.

        Args:
            compendium (CompendiumBase): Compendium object.

            output_directory (Union[str, Path]):

            files (list): A list with the filename to delete.

            kwargs (dict): Extra parameters to the ``storm_client.models.compendium.files.CompendiumFiles.download``.

        Returns:
            Path: Path to the output directory.
        """
        return asyncio.run(
            self._async_download_files(compendium, output_directory, files, **kwargs)
        )
