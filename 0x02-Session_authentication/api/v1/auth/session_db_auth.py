#!/usr/bin/env python3
"""This module contains the SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """Class definition"""
    def create_session(self, user_id=None):
        """This method creates a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session: TypeVar['UserSession'] = UserSession(
            user_id=user_id,
            session_id=session_id
        )
        user_session.save()
        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """This method returns the user_id associated with a session"""
        if super().user_id_for_session_id(session_id) is None:
            if len(self.user_id_by_session_id):
                return None
        sessions = UserSession.search({'session_id': session_id})
        if not len(sessions):
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """This method destroys a session"""
        super().destroy_session(request)
        session_id: str = self.session_cookie(request)
        if not session_id:
            return False

        sessions = UserSession.search({'session_id': session_id})
        if not len(sessions):
            return False

        sessions[0].remove()
        return True
