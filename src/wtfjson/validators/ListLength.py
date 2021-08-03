# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Optional, Any, Union, TYPE_CHECKING

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class ListLength(Validator):
    default_message = 'invalid list length'

    def __init__(self,
                 min_entries: Optional[int] = 0,
                 max_entries: Optional[int] = None,
                 message: Optional[str] = None):
        super().__init__(message)
        self.min_entries = min_entries
        self.max_entries = max_entries

    def __call__(self, value: Any, form: Union['ListInput', 'DictInput'], field: Field):
        if len(value) < self.min_entries or (self.max_entries is not None and len(value) > self.max_entries):
            raise ValidationError(self.message)
