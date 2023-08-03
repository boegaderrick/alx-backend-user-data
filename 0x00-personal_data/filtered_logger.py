#!/usr/bin/env python3
"""Logger module"""
import re


def filter_datum(fields, redaction, msg, sep):
    """Redacts 'msg' values of all keys specified in 'fields'"""
    for i in fields:
        msg = re.sub(f'{i}.*?{sep}', f'{i}={redaction}{sep}', msg)
    return msg
