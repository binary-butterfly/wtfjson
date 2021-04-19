# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from abc import ABC
from typing import List, Any

from .fields import UnboundField
from .validators import Validator
from .exceptions import NotValidated, InvalidData
from .util import unset_value


class DictInput(ABC):
    _fields: dict
    _errors: dict
    _validated: bool = False
    _validators: List[Validator]

    def __init__(self, data: Any):
        # first: init vars
        self._fields = {}
        self._errors = {}
        self._validators = []

        # second: init fields
        for field_name in dir(self):
            if field_name in ['errors', 'has_errors', 'out', 'data']:
                continue
            if isinstance(getattr(self, field_name), UnboundField):
                unbound_field = getattr(self, field_name)
                self._fields[field_name] = unbound_field.bind(self, field_name)
                setattr(self, field_name, self._fields[field_name])

        # third: load data
        for field_name, field in self._fields.items():
            if field_name in data:
                field.process_in(data[field_name])

    def validate(self) -> bool:
        for field_name, field in self._fields.items():
            if not field.validate():
                self._errors.update(field.errors)
        self._validated = True
        return not self.has_errors

    def populate_obj(self, obj):
        if not self._validated:
            raise NotValidated()
        if self.has_errors:
            raise InvalidData()
        for field_name, field in self._fields.items():
            if field.out is not unset_value:
                setattr(obj, field_name, field.out)

    @property
    def has_errors(self) -> bool:
        if not self._validated:
            raise NotValidated()
        return len(self._errors.keys()) > 0

    @property
    def errors(self) -> dict:
        if not self._validated:
            raise NotValidated()
        return self._errors

    @property
    def data(self):
        if not self._validated:
            raise NotValidated()
        if self.has_errors:
            raise InvalidData()
        return {field_name: field.data for field_name, field in self._fields.items()}  #TODO: get fields back

    @property
    def out(self):
        if not self._validated:
            raise NotValidated()
        if self.has_errors:
            raise InvalidData()
        return {field_name: field.out for field_name, field in self._fields.items() if field.out is not unset_value}

