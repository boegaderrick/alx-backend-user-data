#!/usr/bin/env python3
"""This module contains a class that inherits from Auth"""
from api.v1.auth.auth import Auth
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
        except binascii.Error:
            return None
