import logging
from logging.handlers import TimedRotatingFileHandler

log_file = 'app.log'
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Hello')