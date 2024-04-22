from enum import Enum


class Status(Enum):
    OK = 200, 'OK'
    NOT_FOUND = 404, 'Not Found'

    def __init__(self, code, message):
        self.code = code
        self.message = message


PROTOCOL = 'HTTP/1.1'
