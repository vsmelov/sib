import abc

import requests


class TargetBase(abc.ABC):
    @abc.abstractmethod
    def handle(self, request: requests.Request):
        pass

    @abc.abstractmethod
    def close(self):
        pass
