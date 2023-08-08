#!/usr/bin/env python3
"""This module contains the Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require method"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method"""
        return None
