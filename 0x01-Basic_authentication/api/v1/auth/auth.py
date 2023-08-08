#!/usr/bin/env python3
"""This module contains the Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This method checks if 'path' is in 'excluded_paths'"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        return not any(
            i.startswith(path.rstrip('/')) or path.startswith(i.rstrip('*'))
            for i in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Authorization method"""
        if request is None:
            return None
        return request.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method"""
        return None
