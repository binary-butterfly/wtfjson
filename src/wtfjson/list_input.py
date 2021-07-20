# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any
from abc import ABC, abstractmethod

from .exceptions import NotValidated, InvalidData
from .util import unset_value


class ListInput(ABC):
    _fields: list
    _errors: dict
    _validated: bool = False
    _validators: list

    def __init__(self, data: Any):
        if self.field is unset_value:
            raise Exception('field is required')
        # first: init vars
        self._errors = {}
        self._validators = []

        # second: init field
        if type(data) != list:
            self._errors['_root'] = ['invalid type']
            self._validated = True
            return
        self._fields = []
        for i in range(0, len(data)):
            field = self.field.bind(self, str(i))
            field.process_in(data[i])
            self._fields.append(field)

    @property
    @abstractmethod
    def field(self):
        raise NotImplementedError()

    def validate(self) -> bool:
        if self._validated:
            return not self.has_errors
        for field in self._fields:
            if not field.validate():
                self._errors.update(field.errors)
        self._validated = True
        return not self.has_errors

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
        return [field.data for field in self._fields]

    @property
    def out(self):
        if not self._validated:
            raise NotValidated()
        if self.has_errors:
            raise InvalidData()
        return [field.out for field in self._fields if field.out is not unset_value]
