# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any
from . import Validator
from exceptions import ValidationError, InvalidValidator
import Form
from fields import Field
from util import unset_value


class InputRequired(Validator):
    default_message = 'input required'

    def __call__(self, value: Any, form: Form, field: Field):
        if value is not unset_value and type(value) is not str:
            raise InvalidValidator()
        if value is unset_value or len(value) == 0:
            raise ValidationError(self.message)
