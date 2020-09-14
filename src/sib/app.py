import logging

import json
import pickle

import pika
from flask import Flask, request, jsonify

from sib.targets import REGISTERED_TARGETS
from sib.utils.rabbit import get_rabbit_params

logger = logging.getLogger()


def get_app():
    app = Flask(__name__)
    app.connection = pika.BlockingConnection(get_rabbit_params())
    app.channel = app.connection.channel()
    for _target_cls in REGISTERED_TARGETS:
        app.channel.queue_declare(queue=_target_cls.QUEUE)

    @app.route('/', methods=['POST'])
    def index():
        """ pass a request to rabbit """
        for target_cls in REGISTERED_TARGETS:
            try:
                headers = json.dumps(list(request.headers.items()))
                data = request.data
                app.channel.basic_publish(
                    exchange='',
                    routing_key=target_cls.QUEUE,
                    body=pickle.dumps((headers, data)),
                )
                logger.info(f'put request to queue {target_cls.QUEUE} {request.headers=} {request.data=}')
            except Exception as exc:
                logger.exception(f'unhandled publish exception {type(exc)}')
        return jsonify({'text': 'ok'})

    @app.route('/stub', methods=['POST'])
    def stub():
        """ just to check that http worker actually works """
        logger.info(f'STUB: called with {request.headers=} {request.data=}')
        return jsonify({'text': 'ok'})

    return app
