# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
import asyncio

from pydash import py_

from typing import Dict, Union

from storm_hasher import StormHasher

from collections.abc import Sequence
from collections import UserDict, UserList

from ...network import HTTPXClient


def create_file_object(filename: Union[Dict, str]) -> Dict:
    """Create Storm records file entry.

    Args:
        filename (Union[Dict, str]): filename|path to file or invenio file record entry

    Returns:
        Dict: Dict with `filename` formated as Storm-WS file record entry object. The resulting object will have
        the following format:

            {
                "key": filename
            }
    """
    if isinstance(filename, str):
        return {"key": os.path.join(filename)}
    return filename


def map_file_entry(data: Dict, data_path: str):
    """Map all CompendiumBase files entry to a Invenio file record entry.

    Args:
        data (Dict): Dict with the CompendiumBase data.

        data_path (str): Path to the attribute where file entries is on the `data` object.

    Note:
        The file mapping is done in-place on `data` object.
    """
    return py_.set(
        data, data_path, py_.chain(data).get(data_path).map(create_file_object).value()
    )


#
# Compendium files
#
class CompendiumFileEntry(UserDict):
    def __init__(self, data=None):
        super(CompendiumFileEntry, self).__init__(data or {})

    @property
    def filename(self):
        return py_.get(self, "key")

    @property
    def size(self):
        return py_.get(self, "size")

    @property
    def checksum(self):
        return py_.get(self, "checksum")

    @property
    def mimetype(self):
        return py_.get(self, "mimetype")

    @property
    def content_url(self):
        return py_.get(self, "links.content", None)

    @property
    def commit_url(self):
        return py_.get(self, "links.commit", None)

    def download(self, output_directory, validate_checksum=False):
        file_content_link = self.content_url

        if file_content_link:
            os.makedirs(output_directory, exist_ok=True)
            output_file = os.path.join(output_directory, self.filename)

            # download!
            asyncio.run(HTTPXClient.download(file_content_link, output_file))

            if validate_checksum:
                downloaded_file_checksum = StormHasher("md5").hash_file(output_file)

                if downloaded_file_checksum != self.checksum.split(":")[-1]:
                    raise RuntimeError(f"Checksum for {self.filename} is not valid!")

            return output_file
        raise FileNotFoundError("File content is not available!")


class CompendiumFiles(UserList):
    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError("The `data` argument must be a valid sequence type.")

        data = [CompendiumFileEntry(file_entry) for file_entry in py_.get(data, [])]
        super(CompendiumFiles, self).__init__(data)


__all__ = (
    "CompendiumFiles",
    "CompendiumFileEntry",
    "map_file_entry",
    "create_file_object",
)
