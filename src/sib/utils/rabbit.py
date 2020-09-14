import os
import pika


def get_rabbit_params():
    """ make ConnectionParameters to connect to RabbitMQ """
    return pika.ConnectionParameters(
        host=os.environ['RABBIT_HOST'],
        port=int(os.environ.get('RABBIT_PORT', 5672)),
        virtual_host=os.environ['RABBITMQ_DEFAULT_VHOST'],
        credentials=pika.PlainCredentials(
            username=os.environ['RABBITMQ_DEFAULT_USER'],
            password=os.environ['RABBITMQ_DEFAULT_PASS'],
        ),
    )
