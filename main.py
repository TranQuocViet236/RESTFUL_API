import logging
from flask import Flask, request
from logging.handlers import TimedRotatingFileHandler
from flask.logging import create_logger

# logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# import logging
# from logging.handlers import TimedRotatingFileHandler

log_file = 'app.log'
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoggingMiddleware:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger
        self.logger.info('LOG OK')

    def __call__(self, environ, response_callback):
        def log_request(response):
            """Log information about the request and response"""
            user_profile = request.headers.get('user_profile')  # Lấy thông tin profile user từ header
            endpoint = request.endpoint  # Lấy endpoint của request
            headers = dict(request.headers)  # Lấy toàn bộ thông tin header của request
            query = dict(request.args)  # Lấy toàn bộ thông tin query parameters của request
            bodyreq = request.get_data(as_text=True)  # Lấy toàn bộ thông tin body request
            bodyresp = response.get_data(as_text=True)  # Lấy toàn bộ thông tin body response

            # Format log message
            log_msg = f"Endpoint: {endpoint} \nUser Profile: {user_profile} \nHeaders: {headers} \nQuery: {query} \nRequest Body: {bodyreq} \nResponse Body: {bodyresp}"

            # Log message với level là DEBUG
            self.logger.debug(log_msg)
            return response

        def log_response(response):
            """Log information about the response"""
            self.logger.info(f"Response Status Code: {response.status_code} \nResponse Headers: {response.headers}")
            return response

        # Đăng ký hàm log_request và log_response sử dụng decorator after_request
        self.app.after_request(log_request)
        self.app.after_request(log_response)

        # Trả về response callback của Flask
        return self.app(environ, response_callback)


# Khởi tạo middleware LoggingMiddleware và tích hợp vào ứng dụng Flask
logging_middleware = LoggingMiddleware(app, logger)
# logging_middleware = LoggingMiddleware(app, logger)
# app.wsgi_app = logging_middleware

# Route đơn giản để kiểm tra logging middleware hoạt động
@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
