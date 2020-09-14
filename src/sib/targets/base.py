import abc
import logging
import typing as t

logger = logging.getLogger()


class TargetBase(abc.ABC):
    """ Base class for targets """
    QUEUE: str = None

    @classmethod
    @abc.abstractmethod
    def create(cls) -> 'TargetBase':
        """ pain-less way to create an instance """
        pass

    @abc.abstractmethod
    def handle(self, headers: t.Dict[str, str], data: str):
        """ handle the request """
        pass

    @abc.abstractmethod
    def close(self):
        """ close all connections/db/sessions etc """
        pass
