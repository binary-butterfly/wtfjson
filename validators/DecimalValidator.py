# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from decimal import Decimal, InvalidOperation
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class DecimalValidator(Validator):
    default_message = 'invalid decimal'

    def __call__(self, form: Form, field: Field):
        try:
            field.data = Decimal(field.data)
        except InvalidOperation:
            raise ValidationError(self.message)
