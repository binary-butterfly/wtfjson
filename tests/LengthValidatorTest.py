# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""


from unittest import TestCase
from Form import Form
from fields import StringField
from validators import Length


class LengthForm(Form):
    test_field = StringField(
        validators=[
            Length(min=6, max=13)
        ]
    )


class AnyOfValidatorTest(TestCase):
    def test_success_min(self):
        form = LengthForm(data={'test_field': 'cookie'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'cookie'}

    def test_success_max(self):
        form = LengthForm(data={'test_field': 'vanillacookie'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'vanillacookie'}

    def test_invalid_type(self):
        form = LengthForm(data={'test_field': 12})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}

    def test_invalid_value_min(self):
        form = LengthForm(data={'test_field': 'cook'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid length']}

    def test_invalid_value_max(self):
        form = LengthForm(data={'test_field': 'chocolatecookie'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid length']}
