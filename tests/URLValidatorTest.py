# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""


from unittest import TestCase
from Form import Form
from fields import StringField
from validators import URL


class URLForm(Form):
    test_field = StringField(
        validators=[
            URL()
        ]
    )


class URLNoIPForm(Form):
    test_field = StringField(
        validators=[
            URL(allow_ip=False)
        ]
    )


class URLNoTldForm(Form):
    test_field = StringField(
        validators=[
            URL(require_tld=False)
        ]
    )


class URLValidatorTest(TestCase):
    def test_success(self):
        form = URLForm(data={'test_field': 'https://binary-butterfly.de'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'https://binary-butterfly.de'}

    def test_invalid(self):
        form = URLForm(data={'test_field': 'keks'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid url']}

    def test_valid_ip(self):
        form = URLForm(data={'test_field': 'http://10.10.10.10'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'http://10.10.10.10'}

    def test_invalid_ip(self):
        form = URLNoIPForm(data={'test_field': 'http://10.10.10.10'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid url']}

    def test_valid_tld(self):
        form = URLNoTldForm(data={'test_field': 'http://binary-butterfly'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': 'http://binary-butterfly'}

    def test_invalid_tld(self):
        form = URLForm(data={'test_field': 'http://binary-butterfly'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid url']}
