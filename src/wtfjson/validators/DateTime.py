# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Union, TYPE_CHECKING
from datetime import datetime, timezone

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError
if TYPE_CHECKING:
    from ..DictInput import DictInput
    from ..ListInput import ListInput


class DateTime(Validator):
    default_message = 'invalid datetime'

    def __init__(self, localized: bool = False, accept_utc=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.localized = localized
        self.accept_utc = accept_utc

    def __call__(self, value: str, form: Union['DictInput', 'ListInput'], field: Field):
        if not self.localized:
            if self.accept_utc and value[-1] == 'Z':
                value = value[:-1]
            if len(value) != 19:
                raise ValidationError(self.default_message)
            try:
                field.data_processed = datetime.fromisoformat(value)
            except ValueError:
                raise ValidationError(self.message)
            return
        if len(value) < 19:
            raise ValidationError(self.default_message)
        if len(value) in [19, 20]:
            if value[-1] == 'Z':
                value = value[:-1]
            try:
                field.data_processed = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
            except ValueError:
                raise ValidationError(self.message)
            return
        try:
            field.data_processed = datetime.fromisoformat(value)
        except ValueError:
            raise ValidationError(self.message)
