# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any
from decimal import Decimal, InvalidOperation
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class DecimalValidator(Validator):
    default_message = 'invalid decimal'

    def __call__(self, value: Any, form: Form, field: Field):
        try:
            field.data_processed = Decimal(value)
        except InvalidOperation:
            raise ValidationError(self.message)
