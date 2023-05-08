import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request
import json


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
            # print(status.get('code_str'))
            # status_str = status
            status_info = status.split(' ')
            status_code = int(status_info[0])
            status_msg = ' '.join(status_info[1:])

            status_success = True if (status_msg == 'OK') else False
            
            status_obj = {
                'success': status_success,
                'code': status_code,
            }

            if not status_success:
                status_obj.update({'errors': status_msg.lower()})
            
            bodyresp = {
                'status': status_obj
            }
            
            if status_success:
                bodyresp.update({'elements': [request.get_data(as_text=True)]})
            
            bodyresp_str = json.dumps(bodyresp)
            self.logger.info(f'BodyResp: {bodyresp_str}')
            # self.logger.info(f'Status: {status}')
            # print(type(status))
            # print(status)
            # self.logger.info(f"Request: {request.method} {request.url} {status}")
            # self.logger.info(f"Request Headers: {request.headers}")
            # self.logger.info(f"Request Body: {request.get_data(as_text=True)}")
            
            return start_response(status, headers, *args, **kwargs)

        return self.app(environ, _start_response)
