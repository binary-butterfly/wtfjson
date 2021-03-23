# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from typing import Optional
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class Type(Validator):
    default_message = 'invalid type'

    def __init__(self, data_type, message: Optional[str] = None):
        super().__init__(message)
        self.data_type = data_type

    def __call__(self, form: Form, field: Field):
        if type(field.data) is not self.data_type:
            raise ValidationError(self.message)
