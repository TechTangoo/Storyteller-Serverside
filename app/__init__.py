from flask import Flask
from .config import Config
from supabase import create_client, Client

url: str = Config.SUPABASE_API_URL
key: str = Config.SUPABASE_API_KEY

Supabase: Client = create_client(url, key)

app = Flask(__name__)
app.config.from_object(Config)

from app.users import user_bp as user_blueprint

app.register_blueprint(user_blueprint, url_prefix='/user')

from app import views
