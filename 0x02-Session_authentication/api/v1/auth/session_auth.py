#!/usr/bin/env python3
"""This module contains the SessionAuth class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict
from uuid import uuid4


class SessionAuth(Auth):
    """Class definition"""
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a client"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id: str = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id associated with a session"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance associated with a session"""
        session_id: str = self.session_cookie(request)
        user_id: str = self.user_id_for_session_id(session_id)
        return User.get(user_id)
