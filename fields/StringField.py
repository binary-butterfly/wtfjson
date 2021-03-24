# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from fields import Field
from validators import Type


class StringField(Field):
    default_validators = [
        Type(data_type=str)
    ]
