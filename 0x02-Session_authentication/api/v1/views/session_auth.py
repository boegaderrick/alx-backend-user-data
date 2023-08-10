#!/usr/bin/env python3
"""This module contains the login route"""
from api.v1.views import app_views
from flask import jsonify, request, session
from models.user import User
from os import getenv
from typing import TypeVar


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login function definition"""
    email: str = request.form.get('email')
    if not email or len(email) == 0:
        return jsonify({'error': 'email missing'})
    pwd: str = request.form.get('password')
    if not pwd or len(pwd) == 0:
        return jsonify({'error': 'password missing'})

    try:
        users: List[TypeVar['User']] = User.search({'email': email})
    except (AttributeError, Exception):
        users = []
    if len(users) == 0:
        return jsonify({'error': 'no user found for this email'})

    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response

    return jsonify({'error': 'wrong password'})
