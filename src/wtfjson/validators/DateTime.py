# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Union, TYPE_CHECKING
from datetime import datetime

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class DateTime(Validator):
    default_message = 'invalid datetime'

    def __call__(self, value: str, form: Union['DictInput', 'ListInput'], field: Field):
        if len(value) != 19:
            raise ValidationError(self.default_message)
        try:
            field.data_processed = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            raise ValidationError(self.message)
