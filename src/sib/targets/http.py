import logging
import typing as t
import os
import requests

from sib.targets.base import TargetBase
from sib.targets.registered_targets import register_target

logger = logging.getLogger()


@register_target
class TargetHttp(TargetBase):
    QUEUE = 'http'

    @classmethod
    def create(cls):
        return cls(url=os.environ['TARGET_HTTP_URL'])

    def __init__(self, url: str):
        self._url = url

    def handle(self, headers: t.Dict[str, str], data: str):
        logger.info(f'post {headers=} {data=}')
        requests.post(self._url, headers=headers, data=data)

    def close(self):
        pass
