import logging
import os

from sib.targets.base import TargetRunner
from sib.targets.http import TargetHttp
from sib.utils.log import init_log

logger = logging.getLogger()


if __name__ == "__main__":
    init_log(
        console_log_level=os.environ['LOG_CONSOLE_LEVEL'],
        console_log_formatter=os.environ['LOG_CONSOLE_FORMATTER'],
    )
    logger.info('worker http started')
    target = TargetHttp.create()
    runner = TargetRunner(target=target)
    try:
        runner.run()
    finally:
        runner.close()
