# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""


class ValidationError(ValueError):
    message: str

    def __init__(self, message: str):
        self.message = message


class StopValidation(Exception):
    def __init__(self, message: str):
        self.message = message


class ClearValidation(Exception):
    pass


class NotValidated(Exception):
    pass


class InvalidData(Exception):
    pass
