
import aiofiles
import httpx

from storm_client.io import file_chunks_generator


class HTTPXClient:

    @staticmethod
    async def request(method, url, **kwargs):
        """Asynchronous HTTP request.

        Request an URL using the specified HTTP `method`.

        Args:
            method (str): HTTP Method used to request (e.g. `GET`, `POST`, `PUT`, `DELETE`)

            url (str): URL that will be requested

            **kwargs (dict): Extra parameters to `httpx.request` method.

        Returns:
            Coroutine: coroutine to request a site.

        See:
            This method as based on httpx.AsyncClient. Please, check the documentation for more informations: https://www.python-httpx.org/async/

        """
        async with httpx.AsyncClient() as client:
            return await client.request(method, url, **kwargs)

    @staticmethod
    async def upload(method, url, file_path, **kwargs):
        return await HTTPXClient.request(method=method, url=url, data = file_chunks_generator(file_path), **kwargs)

    @staticmethod
    async def download(url, output_file):

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                async with aiofiles.open(output_file, "wb") as ofile:
                    async for chunk in response.aiter_bytes():
                        await ofile.write(chunk)
        return output_file

    # async def get(url, **kwargs):
    #     return await HTTPXClient.request("GET", url, **kwargs)

    # async def post(url, **kwargs):
    #     return await HTTPXClient.request("POST", url, **kwargs)

    # async def put(url, **kwargs):
    #     return await HTTPXClient.request("PUT", url, **kwargs)
