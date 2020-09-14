import json
import pickle
import logging

import pika

from sib.targets import TargetBase
from sib.utils.is_running import is_running
from sib.utils.rabbit import get_rabbit_params

logger = logging.getLogger()


class TargetRunner:
    """ subscribe to a rabbitmq and process it with a target """
    def __init__(self, target: TargetBase):
        self.target = target
        self.connection = pika.BlockingConnection(get_rabbit_params())
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.target.QUEUE)

    def run(self):
        """ run queue messages processing """
        logger.info('Waiting for messages...')
        gen = self.channel.consume(
            queue=self.target.QUEUE,
            inactivity_timeout=1,
        )
        while is_running:
            try:
                method, properties, body = next(gen)
            except StopIteration:
                break
            if (method, properties, body) == (None, None, None):
                continue
            self.on_message_callback(method, properties, body)

    def on_message_callback(self, method, _properties, raw_body):
        """ process the queue message """
        try:
            headers, data = pickle.loads(raw_body)
            headers = json.loads(headers)
            headers = dict(headers)
        except (pickle.UnpicklingError, json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.info(f'{raw_body=}')
            logger.exception(f'bad body {type(exc)}')
            self.channel.basic_ack(delivery_tag=method.delivery_tag)  # remove bad message from the queue
            return
        logger.info(f'receive {headers=} {data=}')
        try:
            self.target.handle(headers, data)
        except Exception as exc:
            logger.exception(f'_on_message_callback exception {type(exc)}')
            self.channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f'processed OK')

    def close(self):
        """ close all connections/db/sessions etc """
        self.channel.close()
        self.connection.close()
        self.target.close()
