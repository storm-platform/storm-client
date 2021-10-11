

from storm_client.services.project import ProjectService


class Storm:

    def __init__(self, url, access_token):
        self._url = url
        self._access_token = access_token

    @property
    def project(self):
        return ProjectService(self._url, self._access_token)
