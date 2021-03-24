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


class AnyOf(Validator):
    default_message = 'is not in any-of list'  # TODO: better message

    def __init__(self, any_of: list, message: Optional[str] = None):
        super().__init__(message)
        self.any_of = any_of

    def __call__(self, value: Any, form: Form, field: Field):
        if value not in self.any_of:
            raise ValidationError(self.message)
