#!/usr/bin/env python3
"""This module contains the UserSession class"""
from models.base import Base
from typing import List


class UserSession(Base):
    """Class definition"""
    def __init__(self, *args: List, **kwargs: dict):
        """Object initialization"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
