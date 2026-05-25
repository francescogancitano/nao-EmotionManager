# -*- coding: utf-8 -*-
import colorlog, logging

_handler = colorlog.StreamHandler()
_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(lineno)d]\t[%(levelname)s] [%(funcName)s]%(reset)s %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))


logger = colorlog.getLogger(__name__)
logger.addHandler(_handler)
logger.setLevel(logging.DEBUG)