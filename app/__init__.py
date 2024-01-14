from flask import Flask
from app.users import bp as user_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint, url_prefix='/user')

from app import views, models
