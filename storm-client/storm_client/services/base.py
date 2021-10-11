
import asyncio
from urllib.parse import urljoin
from storm_client.network import HTTPXClient

from storm_client.object_factory import ObjectFactory


class BaseService:

    def __init__(self, url: str, access_token: str) -> None:
        self._url = url
        self._access_token = access_token

        self._access_token_as_parameter = { "access_token": self._access_token }

    @property
    def url(self):
        return self._url

    @property
    def access_token(self):
        return self._access_token

    def _make_object(self, json):
        return ObjectFactory.make(json)

    def _build_url(self, url):
        return urljoin(self._url, url)

    def _create_request(self, method, url, **kwargs):
        return asyncio.run(HTTPXClient.request(method, url, params=self._access_token_as_parameter, **kwargs))


__all__ = (
    "BaseService"
)
