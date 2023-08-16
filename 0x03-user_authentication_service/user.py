#!/usr/bin/env python3
"""This module contains the User class"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """User class definition"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get('email')
        self.hashed_password = kwargs.get('hashed_password')
