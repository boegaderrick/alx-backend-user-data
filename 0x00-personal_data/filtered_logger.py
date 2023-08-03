#!/usr/bin/env python3
"""Logger module"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redacts 'msg' values of all keys specified in 'fields'"""
    for i in fields:
        message = re.sub(f'{i}.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message
