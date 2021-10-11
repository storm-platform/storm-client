
import aiofiles


async def file_chunks_generator(file_path: str, chunk_size: int = 8192):
    """Read file in chunks.

    Create a chunk generator to read a file. Load as bytes

    Args:
        file_path (str): Path where file is stored.

        chunk_size (int): Chunk size used to load the data.

    Returns:
        Coroutine: coroutine to read the file as chunks.
    """ 
    async with aiofiles.open(file_path, "rb") as file_stream:
        while True:
            chunk_data = await file_stream.read(chunk_size)

            if not chunk_data:
                break
            yield chunk_data


__all__ = (
    "file_chunks_generator"
)
