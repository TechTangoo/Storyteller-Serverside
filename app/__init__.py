from flask import Flask
from .config import Config
from supabase import create_client, Client
from flask_cors import CORS

url: str = Config.SUPABASE_API_URL
key: str = Config.SUPABASE_API_KEY

Supabase: Client = create_client(url, key)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

from app.users import user_bp as user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/user')

from app import views
