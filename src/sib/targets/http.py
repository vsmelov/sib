import os
import requests

from sib.targets.base import TargetBase
from sib.targets.registered_targets import register_target


@register_target
class TargetHttp(TargetBase):
    QUEUE = 'http'

    @classmethod
    def create(cls):
        return cls(url=os.environ['TARGET_HTTP_URL'])

    def __init__(self, url: str):
        self._url = url

    def handle(self, request: requests.Request):
        requests.post(self._url, headers=request.headers, data=request.data)

    def close(self):
        pass
