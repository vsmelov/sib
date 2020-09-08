import requests

from targets.base import TargetBase


class TargetHttp(TargetBase):
    def __init__(self, url: str):
        self._url = url

    def handle(self, request: requests.Request):
        requests.post(self._url, headers=request.headers, data=request.data)

    def close(self):
        pass
