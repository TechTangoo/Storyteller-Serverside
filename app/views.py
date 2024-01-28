from flask import request, jsonify, g, url_for, render_template, redirect
import json
from app import app, Supabase


@app.route("/", methods=['GET'])
def home():
    return "Hello, Hi"


@app.route("/login", methods=['POST'])
def login():
    return 'Loggin succesful'


@app.route("/register", methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        sign_up_response = Supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        if sign_up_response['error'] is not None:
            return jsonify({'error': sign_up_response['error']['message']}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/insert", methods=['POST'])
def insert_data():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user_data = {'email': email, 'passcode': password}
    user_insert_response = Supabase.table('User').insert(user_data).execute()
    print(user_insert_response)
