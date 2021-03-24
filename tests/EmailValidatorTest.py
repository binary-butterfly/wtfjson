# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""


from unittest import TestCase
from Form import Form
from fields import StringField
from validators import Email


class EnumForm(Form):
    test_field = StringField(
        validators=[
            Email()
        ]
    )


class EmailValidatorTest(TestCase):
    def test_success(self):
        form = EnumForm(data={'test_field': 'mail@binary-butterfly.de'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'mail@binary-butterfly.de'}

    def test_invalid_type(self):
        form = EnumForm(data={'test_field': 12})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}

    def test_invalid_mail(self):
        form = EnumForm(data={'test_field': 'binary-butterfly.de'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid email']}
