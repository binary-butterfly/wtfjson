# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Union
from datetime import datetime
from ..fields import Field
from ..validators import Type, DateTime
from ..util import UnsetValue


class DateTimeField(Field):
    def __init__(self, localized: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pre_validators = [
            Type(data_type=str),
            DateTime(localized=localized)
        ]

    @property
    def data(self) -> Union[datetime, UnsetValue]:
        return super().data

    @property
    def out(self) -> Union[datetime, UnsetValue]:
        return super().out
