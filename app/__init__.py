from app import views
from app.story import story_bp as story_blueprint
from app.users import user_bp as user_blueprint
from flask import Flask, jsonify
from .config import Config
from supabase import create_client, Client
from flask_cors import CORS

url: str = Config.SUPABASE_API_URL
key: str = Config.SUPABASE_API_KEY

Supabase: Client = create_client(url, key)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)


@app.route("/", methods=['POST'])
def home():
    return jsonify({'status': 1, 'message': 'server is running at 5000 port'})

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(story_blueprint, url_prefix='/story')
