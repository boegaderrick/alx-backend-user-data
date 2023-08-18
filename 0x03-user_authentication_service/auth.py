#!/usr/bin/env python3
"""This module contains the Auth class"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> bytes:
    """This function takes in a string, encrypts then returns it"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """This function generates UUIDs"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Instantiation method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """This method registers a User object"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """This method validates login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """This method creates a session"""
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: str) -> Union[TypeVar('User'), None]:
        """This method finds and returns a user associated with a session"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """This method destroys a session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """This method sets a user's reset_token attribute"""
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=_generate_uuid())
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """This method updates a user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id,
                hashed_password=_hash_password(password),
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
        return None
