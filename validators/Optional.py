# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from enum import Enum
from typing import Optional, Any
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class Optional(Validator):
    default_message = 'value not in enum'

    def __init__(self, enum: Enum, message: Optional[str] = None):
        super().__init__(message)
        self.enum = enum

    def __call__(self, value: Any, form: Form, field: Field):
        if type(field.data_processed) is not str or not hasattr(self.enum, field.data_processed):
            raise ValidationError(self.message)
        field.data_processed = getattr(self.enum, field.data_processed)
