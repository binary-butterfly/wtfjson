# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from typing import List
from fields import Field
from validators import Validator
from exceptions import NotValidated, InvalidData


class Form:
    _fields: dict
    _errors: dict
    _validated: bool = False
    _validators: List[Validator]

    def __init__(self, data: dict):
        # first: init vars
        self._fields = {}
        self._errors = {}
        self._validators = []

        # second: init fields
        for field_name in dir(self):
            if field_name in ['errors', 'has_errors', 'out']:
                continue
            if isinstance(getattr(self, field_name), Field):
                self._fields[field_name] = getattr(self, field_name)
                self._fields[field_name].init_form(self, field_name)

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

    def populate_obj(self):
        pass

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
    def out(self):
        if not self._validated:
            raise NotValidated()
        if self.has_errors:
            raise InvalidData()
        return {field_name: field.out for field_name, field in self._fields.items()}
