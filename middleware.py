import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app
        log_file = 'app.log'
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def __call__(self, environ, start_response):
        def _start_response(status, headers, *args, **kwargs):
            self.logger.info(f"Request: {request.method} {request.url} {status}")
            self.logger.info(f"Request Headers: {request.headers}")
            self.logger.info(f"Request Body: {request.get_data(as_text=True)}")
            return start_response(status, headers, *args, **kwargs)

        return self.app(environ, _start_response)
