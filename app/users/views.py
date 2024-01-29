from app.users import user_bp
from flask import request, jsonify, g, url_for, render_template, redirect
from app import Supabase
from app.users.functions import hash_password, verify_password


@user_bp.route("/register", methods=['POST'])
def new_user():
    try:
        data = request.get_json() or {}
        username = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        if not email or not password or not username:
            return jsonify({'error': 'Email, username and password are required'}), 400

        hashedpassword = hash_password(password)

        user_data = {'email': email,
                     # Decode bytes to string
                     'passcode': hashedpassword.decode('utf-8'),
                     'user_name': username}

        user_data_res = Supabase.table('User').insert(user_data).execute()

        if user_data_res.data:
            response_data = {'success': True,
                             'message': 'Data inserted successfully'}
            return jsonify(response_data), 201
        else:
            response_data = {'success': False,
                             'message': 'Failed to insert data'}
            return jsonify(response_data), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route("/login", methods=['POST'])  # Change method to POST
def login_user():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Assuming Supabase is properly imported and initialized
        user_data_res = Supabase.table('User').select(
            'passcode').eq('email', email).execute()

        if user_data_res.data:
            hashed_password = user_data_res.data[0].get(
                'passcode').encode('utf-8')
            if verify_password(password, hashed_password):
                response_data = {'success': True,
                                 'message': 'Authentication successful'}
                return jsonify(response_data), 200
            else:
                response_data = {'success': False,
                                 'message': 'Authentication failed'}
                return jsonify(response_data), 401
        else:
            response_data = {'success': False,
                             'message': 'User not found'}
            return jsonify(response_data), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
