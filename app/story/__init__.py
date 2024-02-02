from flask import Blueprint

story_bp = Blueprint('story', __name__)

from app.story import views