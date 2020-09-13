import json
import pickle
import unittest.mock

from sib.targets import TargetRunner


def test_target_runner():
    with unittest.mock.patch('pika.BlockingConnection', unittest.mock.MagicMock()), \
         unittest.mock.patch('sib.targets.base.get_rabbit_params', unittest.mock.MagicMock()):
        runner = TargetRunner(target=unittest.mock.MagicMock())
        runner.channel = unittest.mock.MagicMock()
        headers = ['Some', 'Value']
        data = '{"key": "value"}'
        gen = iter([
            (unittest.mock.MagicMock(), unittest.mock.MagicMock(), pickle.dumps((json.dumps(headers), data)))
        ])
        runner.channel.consume = unittest.mock.MagicMock(return_value=gen)
        runner.run()
        runner.target.handle.assert_called_once_with(headers, data)
