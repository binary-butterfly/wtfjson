# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from unittest import TestCase
from wtfjson import DictInput
from wtfjson.fields import IntegerField, StringField
from wtfjson.validators import Length


class OptionalDictInput(DictInput):
    test_field = IntegerField(required=False)


class RequiredDictInput(DictInput):
    test_field = StringField(
        validators=[
            Length(min=1)
        ]
    )


class OptionalRequiredTest(TestCase):
    def test_optional(self):
        form = OptionalDictInput(data={})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {}

    def test_required_error(self):
        form = RequiredDictInput(data={})
        assert form.validate() is False
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['data required']}

    def test_required_success(self):
        form = RequiredDictInput(data={'test_field': 'cookies'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'cookies'}
