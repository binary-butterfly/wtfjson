# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any, Union, TYPE_CHECKING
from email_validator import validate_email, EmailNotValidError

from ..validators import Validator
from ..exceptions import ValidationError
from ..fields import Field
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class Email(Validator):
    default_message = 'invalid email'

    def __call__(self, value: Any, form: Union['DictInput', 'ListInput'], field: Field):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValidationError(self.message)
