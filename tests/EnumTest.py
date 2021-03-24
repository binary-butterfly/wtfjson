# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""



from enum import Enum
from unittest import TestCase
from Form import Form
from fields import EnumField


class TestEnum(Enum):
    apple = 'juicy apple'
    lemon = 'fresh lemon'


class EnumForm(Form):
    test_field = EnumField(TestEnum)


class EnumTest(TestCase):
    def test_success(self):
        form = EnumForm(data={'test_field': 'apple'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': TestEnum.apple}

    def test_missing_enum(self):
        form = EnumForm(data={'test_field': 'kekse'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['value not in enum']}

    def test_invalid_type(self):
        form = EnumForm(data={'test_field': 10})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type', 'value not in enum']}
