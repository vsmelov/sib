import os

import logging

from sib.app import get_app
from sib.utils.log import init_log

logger = logging.getLogger()

if __name__ == "__main__":
    init_log(
        console_log_level=os.environ['LOG_CONSOLE_LEVEL'],
        console_log_formatter=os.environ['LOG_CONSOLE_FORMATTER'],
    )
    logger.info('web started')
    port = int(os.environ["FLASK_PORT"])
    app = get_app()
    try:
        app.run(host=os.environ["FLASK_HOST"], port=port)
    finally:
        app.channel.close()
        app.connection.close()
