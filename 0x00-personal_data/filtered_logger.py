#!/usr/bin/env python3
"""Logger module"""
from typing import List
import logging
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redacts 'msg' values of all keys specified in 'fields'"""
    for i in fields:
        message = re.sub(f'{i}.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            This method takes a log record, calls a function that redacts the
            values of keys specified in 'FIELDS' attribute then passes the new
            redacted log to the parent class' format method. The parents method's
            return value is then returned to the original caller.
        """
        record.msg = filter_datum(self.FIELDS, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)
