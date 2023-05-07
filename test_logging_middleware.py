from middleware import LoggingMiddleware
from flask import Flask
# from logging_middleware import LoggingMiddleware

app = Flask(__name__)
app.wsgi_app = LoggingMiddleware(app.wsgi_app)

# Route đơn giản để kiểm tra middleware hoạt động
@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

