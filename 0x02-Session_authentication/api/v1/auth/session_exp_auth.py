#!/usr/bin/env python3
"""This module contains the SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from typing import TypeVar


class SessionExpAuth(SessionAuth):
    """Class definition"""
    def __init__(self):
        """SessionExpAuth instantation"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """This method creates a session and attaches a timestamp to it"""
        session_id: str = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'session dictionary': {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """This method return a user_id"""
        if session_id is None:
            return None
        session_dictionary: Dict = self.user_id_by_session_id.get(
            session_id)['session dictionary']
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at: TypeVar['datetime'] = session_dictionary.get('created_at')
        if created_at is None:
            return None
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None

        return session_dictionary.get('user_id')
