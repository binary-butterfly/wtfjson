# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from enum import Enum
from typing import Optional
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class EnumValidator(Validator):
    default_message = 'value not in enum'

    def __init__(self, enum: Enum, message: Optional[str] = None):
        super().__init__(message)
        self.enum = enum

    def __call__(self, form: Form, field: Field):
        if type(field.data) is not str or not hasattr(self.enum, field.data):
            raise ValidationError(self.message)
        field.data = getattr(self.enum, field.data)
