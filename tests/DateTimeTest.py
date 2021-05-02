# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from datetime import datetime, timezone, timedelta
from unittest import TestCase
from wtfjson import DictInput
from wtfjson.fields import DateTimeField


class DateDictInput(DictInput):
    test_field = DateTimeField()


class LocalizedDateDictInput(DictInput):
    test_field = DateTimeField(localized=True)


class DateTimeTest(TestCase):
    def test_success(self):
        form = DateDictInput(data={'test_field': '2020-10-01T10:10:12'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': datetime(2020, 10, 1, 10, 10, 12)}

    def test_localized_success(self):
        form = LocalizedDateDictInput(data={'test_field': '2020-10-01T10:10:12'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': datetime(2020, 10, 1, 10, 10, 12, tzinfo=timezone.utc)}

    def test_localized_success_with_z(self):
        form = LocalizedDateDictInput(data={'test_field': '2020-10-01T10:10:12Z'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': datetime(2020, 10, 1, 10, 10, 12, tzinfo=timezone.utc)}

    def test_localized_success_with_z(self):
        form = LocalizedDateDictInput(data={'test_field': '2020-10-01T10:10:12+02:00'})
        assert form.validate() is True
        assert form.has_errors is False
        assert form.errors == {}
        assert form.out == {'test_field': datetime(2020, 10, 1, 10, 10, 12, tzinfo=timezone(timedelta(seconds=7200)))}

    def test_invalid_type(self):
        form = DateDictInput(data={'test_field': 1})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid type']}

    def test_invalid_format(self):
        form = DateDictInput(data={'test_field': '2020-1x-30T10:10:10'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid datetime']}

    def test_invalid_date(self):
        form = DateDictInput(data={'test_field': '2020-10-40T10:10:70'})
        assert form.validate() is False
        assert form.has_errors is True
        assert form.errors == {'test_field': ['invalid datetime']}
