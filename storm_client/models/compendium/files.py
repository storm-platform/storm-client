# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path
from typing import Union

from storm_hasher import StormHasher

from ..base import BaseModel
from ...network import HTTPXClient
from ...field import DictField, ObjectCollectionField, ObjectField


class CompendiumFiles(BaseModel):
    """Compendium Files."""

    enabled = DictField("enabled")
    """Flag indicating if file is enabled."""

    entries = ObjectCollectionField("entries", "CompendiumFileMetadata")
    """Compendium file entries."""

    def __init__(self, data=None):
        super(CompendiumFiles, self).__init__(data or {})


class CompendiumFileMetadata(BaseModel):
    """Compendium file metadata."""

    #
    # Data fields
    #

    # General informations
    id = DictField("file_id")
    """File ID."""

    filename = DictField("key")
    """Filename."""

    version_id = DictField("version_id")
    """File version ID."""

    # Metadata
    size = DictField("size")
    """File size (in bytes)."""

    mimetype = DictField("mimetype")
    """File mimetype."""

    checksum = DictField("checksum")
    """File checksum (md5)."""

    status = DictField("status")
    """The files can have two status:
            - completed: Ingestion and checksum validation complete;
            - pending: Is defined but the ingestion has not been done.
    """

    # Bucket
    bucket_id = DictField("bucket_id")
    """File bucket where is stored in the service."""

    # Links
    links = ObjectField("links", "CompendiumFileLink")
    """Compendium record links."""

    def __init__(self, data=None):
        super(CompendiumFileMetadata, self).__init__(data or {})

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
        file_content_link = self.links.content

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
