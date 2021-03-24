# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""



from unittest import TestCase
from Form import Form
from fields import IntegerField


class IntegerForm(Form):
    test_field = IntegerField()


class IntegerTest(TestCase):
    def test_success(self):
        form = IntegerForm(data={'test_field': 20})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 20}

    def test_invalid(self):
        form = IntegerForm(data={'test_field': 'string'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}
