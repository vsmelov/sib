import pickle
import unittest.mock
import json

import pytest

from sib.app import get_app
from sib.targets.registered_targets import REGISTERED_TARGETS


@pytest.fixture
def client():
    with unittest.mock.patch('pika.BlockingConnection', unittest.mock.MagicMock()),\
            unittest.mock.patch('daemons.web.get_rabbit_params', unittest.mock.MagicMock()):
        app = get_app()
        app.testing = True
        app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_some_request(client):
    """Start with a blank database."""
    headers = [['Some', 'Value']]
    data = '{"x": 42}'
    rv = client.post('/', headers=headers, data=data)
    assert rv.data == b'{"text":"ok"}\n'
    call_args_list = client.application.channel.basic_publish.call_args_list
    assert len(call_args_list) > 0
    assert len(call_args_list) == len(REGISTERED_TARGETS)
    for target_cls in REGISTERED_TARGETS:
        args = next(c for c in call_args_list if c.kwargs['routing_key'] == target_cls.QUEUE)
        kwargs = args.kwargs
        assert kwargs['exchange'] == ''
        assert kwargs['routing_key'] == target_cls.QUEUE
        request_headers, request_data = pickle.loads(kwargs['body'])
        request_headers = json.loads(request_headers)
        for header in headers:
            assert header in request_headers
        assert request_data == data.encode()
