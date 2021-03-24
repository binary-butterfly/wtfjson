# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""


from unittest import TestCase
from Form import Form
from fields import StringField


class StringForm(Form):
    test_field = StringField()


class StringTest(TestCase):
    def test_success(self):
        form = StringForm(data={'test_field': 'string'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'string'}

    def test_invalid(self):
        form = StringForm(data={'test_field': 20})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}
