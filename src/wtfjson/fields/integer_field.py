# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Union

from ..fields import Field
from ..validators import Type
from ..util import UnsetValue


class IntegerField(Field):
    pre_validators = [
        Type(data_type=int)
    ]

    @property
    def data(self) -> Union[int, UnsetValue]:
        return super().data

    @property
    def out(self) -> Union[int, UnsetValue]:
        return super().out
