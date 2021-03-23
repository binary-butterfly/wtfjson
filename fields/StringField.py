# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from fields import Field
from validators import Type


class StringField(Field):
    default_validators = [
        Type(data_type=str)
    ]
