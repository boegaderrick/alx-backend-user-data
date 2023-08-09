#!/usr/bin/env python3
"""This module contains a class that inherits from Auth"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import List, TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """Class definition"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            This method extracts the encoded authentication credentials
            from the header value and returns it.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """This method decodes the base64 header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            ret = base64.b64decode(base64_authorization_header)
            return ret.decode()
        except (binascii.Error, Exception):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """This method extracts credentials from the decoded string"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Gets the user associated with provided credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users: List[TypeVar('User')] = User.search({'email': user_email})
        except Exception:
            return None
        if len(users) < 1:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This method retrieves the current user"""
        if request is None:
            return None

        header: str = self.authorization_header(request)
        if header is None:
            return None

        creds_bs64: str = self.extract_base64_authorization_header(header)
        if creds_bs64 is None:
            return None

        creds_str: str = self.decode_base64_authorization_header(creds_bs64)
        if creds_str is None:
            return None

        creds: Tuple(str, str) = self.extract_user_credentials(creds_str)
        if any(cred is None for cred in creds):
            return None

        user: TypeVar('User') = self.user_object_from_credentials(*creds)

        return user
