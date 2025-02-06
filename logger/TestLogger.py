import logging
from logging import config

logging.config.fileConfig('logging.ini')
logger1 = logging.getLogger('name1')
logger2 = logging.getLogger('name2')

logger1.debug('This is logger1')
logger2.info('This is logger2')
logger1.warning('This is logger1')
logger1.error('This is logger1')
logger2.warning('This is logger2')
logger2.error('This is logger2')
