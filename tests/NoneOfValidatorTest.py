# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""


from unittest import TestCase
from Form import Form
from fields import StringField
from validators import NoneOf


class EnumForm(Form):
    test_field = StringField(
        validators=[
            NoneOf(['cookie'])
        ]
    )


class NoneOfValidatorTest(TestCase):
    def test_success(self):
        form = EnumForm(data={'test_field': 'chocolate'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'chocolate'}

    def test_invalid_type(self):
        form = EnumForm(data={'test_field': 12})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}

    def test_invalid_value(self):
        form = EnumForm(data={'test_field': 'cookie'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['is in none-of list']}
