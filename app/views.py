from flask import request, jsonify, g, url_for, render_template, redirect
import json
from app import app


@app.route("/", methods=['GET'])
def home():
    return "Hello, Hi"
