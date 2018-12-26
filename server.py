from flask import Flask
from api.predict_api import predict_api
app = Flask(__name__)
app.register_blueprint(predict_api)
