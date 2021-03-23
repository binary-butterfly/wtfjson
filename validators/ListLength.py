# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from typing import Optional
import Form
from fields import Field
from validators import Validator
from exceptions import ValidationError


class ListLength(Validator):
    default_message = 'invalid list length'

    def __init__(self,
                 min_entries: Optional[int] = 0,
                 max_entries: Optional[int] = None,
                 message: Optional[str] = None):
        super().__init__(message)
        self.min_entries = min_entries
        self.max_entries = max_entries

    def __call__(self, form: Form, field: Field):
        if len(field.data) < self.min_entries or (self.max_entries is not None and len(field.data) < self.max_entries):
            raise ValidationError(self.message)
