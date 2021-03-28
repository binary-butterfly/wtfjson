# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Optional, Any, Union, TYPE_CHECKING

from ..fields import Field
from ..validators import Validator
from ..exceptions import StopValidation
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class Type(Validator):
    default_message = 'invalid type'

    def __init__(self, data_type, message: Optional[str] = None):
        super().__init__(message)
        self.data_type = data_type

    def __call__(self, value: Any, form: Union['DictInput', 'ListInput'], field: Field):
        if type(value) is not self.data_type:
            raise StopValidation(self.message)
