# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""



from unittest import TestCase
from Form import Form
from fields import StringField, ObjectField, IntegerField


class SubObjectForm(Form):
    test_field_string = StringField()
    test_field_int = IntegerField()


class ObjectForm(Form):
    test_field = ObjectField(SubObjectForm)


class ObjectTest(TestCase):
    def test_success(self):
        form = ObjectForm(data={'test_field': {'test_field_string': 'lecker', 'test_field_int': 10}})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': {'test_field_string': 'lecker', 'test_field_int': 10}}

    def test_no_object(self):
        form = ObjectForm(data={'test_field': 'nanana'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}

    def test_invalid_sub_field(self):
        form = ObjectForm(data={'test_field': {'test_field_string': 'lecker', 'test_field_int': '10'}})
        assert form.validate() is False
        assert form.has_errors is True
        print(form.errors)
        assert form.errors == {'test_field.test_field_int': ['invalid type']}
