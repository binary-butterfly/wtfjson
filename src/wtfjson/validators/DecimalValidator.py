# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any, Union, TYPE_CHECKING
from decimal import Decimal, InvalidOperation

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class DecimalValidator(Validator):
    default_message = 'invalid decimal'

    def __call__(self, value: Any, form: Union['ListInput', 'DictInput'], field: Field):
        try:
            field.data_processed = Decimal(value)
        except InvalidOperation:
            raise ValidationError(self.message)
