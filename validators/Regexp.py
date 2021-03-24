# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

import re
from typing import Any, Optional, Union, Pattern, Match
from . import Validator
from exceptions import ValidationError
import Form
from fields import Field


class Regexp(Validator):
    rule: Pattern
    default_message = 'regexp failed'

    def __init__(self, rule: Union[str, Pattern], flags: int = 0, message: Optional[str] = None):
        super().__init__(message)
        self.rule = rule if type(rule) is Pattern else re.compile(rule, flags)

    def __call__(self, value: Any, form: Form, field: Field) -> Match:
        match = self.rule.match(value)
        if match is None:
            raise ValidationError(self.message)
        return match
