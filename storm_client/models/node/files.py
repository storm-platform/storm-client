#
# This file is part of SpatioTemporal Open Research Manager.
# Copyright (C) 2021 INPE.
#
# SpatioTemporal Open Research Manager is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import os
import asyncio

from collections.abc import Sequence
from collections import UserDict, UserList

from pydash import py_

from storm_client.network import HTTPXClient


#
# Node files
#
class NodeFileEntry(UserDict):
    def __init__(self, data=None):
        super(NodeFileEntry, self).__init__(data or {})

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

    # ToDo: Implement the checksum validation
    def download(self, output_directory, validate_checksum=False):
        file_content_link = self.content_url

        if file_content_link:
            os.makedirs(output_directory, exist_ok=True)
            output_file = os.path.join(output_directory, self.filename)

            # download!
            asyncio.run(HTTPXClient.download(file_content_link, output_file))
            return output_file
        raise FileNotFoundError("File content is not available!")


class NodeFiles(UserList):

    def __init__(self, data=None):
        if not isinstance(data, Sequence):
            raise ValueError('The `data` argument must be a valid sequence type.')

        data = [NodeFileEntry(file_entry) for file_entry in py_.get(data, [])]
        super(NodeFiles, self).__init__(data)


__all__ = (
    "NodeFiles",
    "NodeFileEntry"
)
