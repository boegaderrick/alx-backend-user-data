#!/usr/bin/env python3
"""This module contains functions that encrypt and validate passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Takes a password string, encrypts and returns it"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password string matches encrypted password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
