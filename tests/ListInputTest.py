# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from unittest import TestCase
from wtfjson import ListInput
from wtfjson.fields import StringField


class StringListInput(ListInput):
    field = StringField()


class ListInputTest(TestCase):
    def test_success(self):
        form = StringListInput(['keks', 'lecker'])
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == ['keks', 'lecker']

    def test_no_list(self):
        form = StringListInput('cookie')
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'_root': ['invalid type']}

    def test_wrong_list_entry(self):
        form = StringListInput(['keks', 123])
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'1': ['invalid type']}
