#!/usr/bin/env python3
"""This module contains a simple flask app"""
from auth import Auth
from flask import abort, Flask, jsonify, make_response, request

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """This method serves content for the home address"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return make_response(
            jsonify({'email': email, 'message': 'user created'}), 200)
    except ValueError:
        return make_response(
            jsonify({'message': 'email already registered'}), 400)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """This function performs logins"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(
        jsonify({'email': email, 'message': 'logged in'}), 200)
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """This function perfoms logouts"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return home()


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """This function gets user associated with a session"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return make_response(jsonify({'email': user.email}), 200)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """This function returns a user's password reset token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return make_response(
            jsonify({'email': email, 'reset_token': token}), 200)
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """This function updates a user's password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return make_response(
        jsonify({'email': email, 'message': 'password updated'}), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
