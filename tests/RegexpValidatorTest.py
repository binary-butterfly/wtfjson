# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

import re
from unittest import TestCase
from Form import Form
from fields import StringField
from validators import Regexp


class RegexpPatternForm(Form):
    test_field = StringField(
        validators=[
            Regexp(re.compile(r'\d+\w+'))
        ]
    )


class RegexpStringForm(Form):
    test_field = StringField(
        validators=[
            Regexp(r'\d+\w+')
        ]
    )


class RegexpValidatorTest(TestCase):
    def test_success_pattern(self):
        form = RegexpPatternForm(data={'test_field': '1cookie'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': '1cookie'}

    def test_success_string(self):
        form = RegexpStringForm(data={'test_field': '1cookie'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': '1cookie'}

    def test_invalid_mail(self):
        form = RegexpPatternForm(data={'test_field': 'cookie'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['regexp failed']}
