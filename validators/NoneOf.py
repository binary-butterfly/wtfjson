# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any, Optional
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class NoneOf(Validator):
    default_message = 'is in none-of list'  # TODO: better message

    def __init__(self, none_of: list, message: Optional[str] = None):
        super().__init__(message)
        self.none_of = none_of

    def __call__(self, value: Any, form: Form, field: Field):
        if value in self.none_of:
            raise ValidationError(self.message)
