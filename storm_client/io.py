# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-client is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def file_chunks_generator(file_path: str, chunk_size: int = 8192):
    """Read file in chunks.

    Create a chunk generator to read a file. Load as bytes.

    Args:
        file_path (str): Path where file is stored.

        chunk_size (int): Chunk size used to load the data (Default 8192).

    Returns:
        Generator: Generator with the file chunks.
    """
    with open(file_path, "rb") as file_stream:
        while True:
            chunk_data = file_stream.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data
