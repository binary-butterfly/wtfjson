# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from enum import Enum
from typing import Optional, Any, Union, TYPE_CHECKING, Type

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class EnumValidator(Validator):
    default_message = 'value not in enum'

    def __init__(self, enum: Type[Enum], message: Optional[str] = None):
        super().__init__(message)
        self.enum: Type[Enum] = enum

    def __call__(self, value: Any, form: Union['DictInput', 'ListInput'], field: Field):
        if type(field.data_processed) is not str or field.data_processed not in [item.value for item in self.enum]:
            raise ValidationError(self.message)
        field.data_processed = self.enum(field.data_processed)
