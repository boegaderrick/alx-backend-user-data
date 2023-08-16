#!/usr/bin/env python3
"""This module contains tests for endpoints"""
import requests

url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """This function tests the '/users' endpoint"""
    data = {'email': email, 'password': password}
    response = requests.post(url + '/users', data=data)
    if response.status_code == 200:
        assert response.json() == {
            'email': email,
            'message': 'user created'
        }
    elif response.status_code == 400:
        assert response.json() == {
            'message': 'email already registered'
        }


def log_in_wrong_password(email: str, password: str) -> None:
    """This function tests login with wrong credentials"""
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """This function tests login with correct credentials"""
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {
        'email': email,
        'message': 'logged in'
    }
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """This function tests '/profile' without passing session_id"""
    response = requests.get(url + '/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """This function tests '/profile' with valid session_id"""
    response = requests.get(
        url + '/profile', cookies={'session_id': session_id})
    assert response.json() == {'email': EMAIL}
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """This function tests the logout"""
    response = requests.delete(
        url + '/sessions', cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """This function tests the '/reset_password' endpoint"""
    response = requests.post(url + '/reset_password', data={'email': email})
    assert response.status_code == 200
    assert response.json().get('email') == email
    token = response.json().get('reset_token')
    assert type(token) is str and len(token) == 36 and token.count('-') == 4
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """This function tests the update password endpoint"""
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url + '/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {
        'email': email, 'message': 'password updated'
    }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
