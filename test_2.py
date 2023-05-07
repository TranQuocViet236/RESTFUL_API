import logging
from flask import Flask, request

app = Flask(__name__)

# Khởi tạo logger
from logging.handlers import TimedRotatingFileHandler

log_file = 'app.log'
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Middleware logging
@app.before_request
def log_request_info():
    logger.info('Start request: %s %s', request.method, request.url)
    logger.info('Request headers: %s', request.headers)
    logger.info('Request body: %s', request.get_data())

@app.after_request
def log_response_info(response):
    logger.info('Response status: %s', response.status)
    logger.info('Response headers: %s', response.headers)
    logger.info('Response body: %s', response.get_data())
    return response

# Route đơn giản để kiểm tra logging middleware hoạt động
@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
