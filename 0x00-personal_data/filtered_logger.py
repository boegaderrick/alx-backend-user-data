#!/usr/bin/env python3
"""Logger module"""
import re


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    """Redacts 'msg' values of all keys specified in 'fields'"""
    for i in fields:
        msg = re.sub(f'{i}.*?{sep}', f'{i}={redaction}{sep}', msg)
    return msg
