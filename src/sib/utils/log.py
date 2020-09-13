import logging


def init_log(console_log_level='INFO', console_log_formatter='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """ initialise logging system """
    logger = logging.getLogger()
    logger.setLevel(console_log_level)
    sh = logging.StreamHandler()
    sh.setLevel(console_log_level)
    sh_fmt = logging.Formatter(console_log_formatter)
    sh.setFormatter(sh_fmt)
    logger.addHandler(sh)
