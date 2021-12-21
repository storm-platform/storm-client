# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path
from typing import Union

from pydash import py_
from storm_hasher import StormHasher

from ..base import BaseModel
from ...network import HTTPXClient


class CompendiumFiles(BaseModel):
    """Compendium Files."""

    def __init__(self, data=None):
        super(CompendiumFiles, self).__init__(data or {})

    @property
    def enabled(self):
        """File entry filename."""
        return self.get_field("enabled")

    @property
    def entries(self):
        """Compendium file entries."""
        return py_.map(self.get_field("entries"), CompendiumFileMetadata)


class CompendiumFileMetadata(BaseModel):
    """Compendium file metadata."""

    def __init__(self, data=None):
        super(CompendiumFileMetadata, self).__init__(data or {})

    @property
    def filename(self):
        """File filename."""
        return self.get_field("key")

    @property
    def status(self):
        """File status.

        Note:
            The files can have two status:
                - completed: Ingestion and checksum validation complete;
                - pending: Is defined but the ingestion has not been done.
        """
        return self.get_field("status")

    @property
    def size(self):
        """File size."""
        return self.get_field("size")

    @property
    def checksum(self):
        """File checksum (md5)."""
        return self.get_field("checksum")

    @property
    def mimetype(self):
        """File mimetype."""
        return self.get_field("mimetype")

    @property
    def url(self):
        """File URL."""
        return self.get_field("links.self")

    @property
    def content_url(self):
        """File content url (to download)."""
        return self.get_field("links.content")

    async def download(
        self, output_directory: Union[str, Path], validate_checksum: bool = False
    ):
        """Download the file entry content.

        Args:
            output_directory (Union[str, Path]): Directory where the content file will be saved.

            validate_checksum (bool): Flag indicating if the file content must be validate with the
                                      checksum provided by the Storm WS.
        """
        output_directory = Path(output_directory)
        file_content_link = self.content_url

        if file_content_link:
            output_file = output_directory / self.filename

            # download!
            await HTTPXClient.download(file_content_link, output_file)

            if validate_checksum:
                # md5 is fixed on `Storm WS`.
                downloaded_file_checksum = StormHasher("md5").hash_file(output_file)

                if downloaded_file_checksum != self.checksum.split(":")[-1]:
                    raise RuntimeError(f"Checksum for {self.filename} is not valid!")

            return output_file
        raise FileNotFoundError("File content is not available!")
