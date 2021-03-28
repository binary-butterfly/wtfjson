# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from decimal import Decimal
from unittest import TestCase
from wtfjson import DictInput
from wtfjson.fields import DecimalField


class EnumDictInput(DictInput):
    test_field = DecimalField()


class EnumTest(TestCase):
    def test_success(self):
        form = EnumDictInput(data={'test_field': '1.3'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': Decimal('1.3')}

    def test_char_string_input(self):
        form = EnumDictInput(data={'test_field': 'cookie'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid decimal']}

    def test_float_input(self):
        form = EnumDictInput(data={'test_field': 1.3})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}
