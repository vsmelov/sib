import typing as t

from sib.targets.base import TargetBase

REGISTERED_TARGETS: t.List[TargetBase] = []


def register_target(target_cls):
    """ register target """
    assert target_cls not in REGISTERED_TARGETS
    REGISTERED_TARGETS.append(target_cls)
    return target_cls
