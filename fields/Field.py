# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from copy import deepcopy
from typing import List, Callable, Optional, Any
from validators import Validator
from util import unset_value
from exceptions import ValidationError, StopValidation, ClearValidation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import Form


class Field:
    _form: 'Form'
    data_raw: Any
    data: Any
    out: Any
    description: Optional[str]
    input_filters: Optional[List[Callable]]
    default_input_filters: List[Callable] = []
    output_filters: Optional[List[Callable]]
    default_output_filters = List[Callable]
    validators: Optional[List[Validator]]
    default_validators: List[Validator] = []
    _errors: dict

    def __init__(self,
                 description: Optional[str] = None,
                 input_filters: Optional[List[Callable]] = None,
                 output_filters: Optional[List[Callable]] = None,
                 validators: Optional[List[Validator]] = None):
        self.description = description
        self.input_filters = input_filters if input_filters is not None else []
        self.output_filters = output_filters if output_filters is not None else []
        self.validators = validators if validators is not None else []
        self.data_raw = unset_value
        self._data = unset_value
        self._out = unset_value

    def init_form(self, form: 'Form', field_name):
        self._errors = {}
        self._form = form
        self._field_name = field_name

    def process_in(self, data_raw: Any):
        self.data_raw = data_raw
        self._data = deepcopy(self.data_raw)
        for input_filter in self.default_input_filters + self.input_filters:
            self._data = input_filter(self._data)

    def validate(self) -> bool:
        try:
            for validator in self.default_validators + self.validators:
                try:
                    validator(self._form, self)
                except ValidationError as error:
                    self.append_error(error.message)
        except StopValidation as error:
            self.append_error(error.message)
        except ClearValidation as no_error:
            self._errors = {}
        self.process_out()
        return not self.has_errors

    def append_error(self, error: str):
        if self._field_name not in self._errors:
            self._errors[self._field_name] = []
        self._errors[self._field_name].append(error)

    def process_out(self):
        self._out = self.data
        for output_filter in self.default_input_filters + self.output_filters:
            self._out = output_filter(self.out)

    @property
    def errors(self) -> dict:
        return self._errors

    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def data(self):
        return self._data

    @property
    def out(self):
        return self._data
