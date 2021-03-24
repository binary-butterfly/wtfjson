# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from enum import Enum
from copy import deepcopy
from typing import List, Callable, Optional, Any, Type, TypeVar
from validators import Validator
from util import unset_value
from exceptions import ValidationError, StopValidation, ClearValidation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import Form


class FieldState(Enum):
    initialized = 1
    processed = 2
    loaded = 3
    validated = 4


class Field:
    state: FieldState
    _form: 'Form'
    _field_name: str
    data_raw: Any  # raw input data
    data_processed: Any  # data after input filters
    data_out: Any  # data after output filters
    description: Optional[str]
    input_filters: Optional[List[Callable]]
    default_input_filters: List[Callable] = []
    output_filters: Optional[List[Callable]]
    default_output_filters = List[Callable]
    validators: Optional[list]
    default_validators: list = []
    pre_validators: list = []
    validation_stopped: bool
    _errors: dict

    def __init__(self,
                 description: Optional[str] = None,
                 input_filters: Optional[list] = None,
                 output_filters: Optional[list] = None,
                 validators: Optional[list] = None):
        self.description = description
        self.input_filters = input_filters if input_filters is not None else []
        self.output_filters = output_filters if output_filters is not None else []
        self.validators = validators if validators is not None else []

    def init_form(self, form: 'Form', field_name):
        """
        runs when the form is initialized (usually at an endpoint)
        """
        self._errors = {}
        self._form = form
        self._field_name = field_name
        self.state = FieldState.initialized
        self.data_raw = unset_value
        self.data_processed = unset_value
        self.data_out = unset_value
        self.validation_stopped = False

    def process_in(self, data_raw: Any):
        """
        after initializing the form the data is added in a raw form and is processed afterwards
        """
        self.data_raw = deepcopy(data_raw)
        self.data_processed = deepcopy(self.data_raw)
        for input_filter in self.default_input_filters + self.input_filters:
            self.data_processed = input_filter(self.data_processed)
        self.state = FieldState.processed
        self.pre_validate()

    def pre_validate(self):
        """
        this validator runs before turning data into objects / lists / ...
        """
        try:
            for validator in self.pre_validators:
                try:
                    validator(self.data_processed, self._form, self)
                except ValidationError as error:
                    self.append_error(error.message)
        except StopValidation as error:
            self.append_error(error.message)
            self.validation_stopped = True
        except ClearValidation as no_error:
            self._errors = {}
            self.validation_stopped = False

    def validate(self) -> bool:
        """
        the primary validator which runs default validators of the field and additional validators given by the form
        definition
        """
        if self.validation_stopped is True:
            self.state = FieldState.validated
            return not self.has_errors
        try:
            for validator in self.default_validators + self.validators:
                try:
                    validator(self.data, self._form, self)
                except ValidationError as error:
                    self.append_error(error.message)
        except StopValidation as error:
            self.append_error(error.message)
            self.validation_stopped = True
        except ClearValidation as no_error:
            self._errors = {}
            self.validation_stopped = False
        self.state = FieldState.validated
        return not self.has_errors

    def append_error(self, error: str):
        if self._field_name not in self._errors:
            self._errors[self._field_name] = []
        self._errors[self._field_name].append(error)

    @property
    def errors(self) -> dict:
        """
        errors are always flat dictionaries. nested errors are separated by dots like
        bakery.cookies.1.flavor = 'chocolate'
        """
        return self._errors

    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def data(self):
        """
        data is the primary interface to anything from outside wanting to access data of fields
        """
        return self.data_processed

    @property
    def out(self):
        """
        out is quite the same as data, but after output filters
        """
        if self.data_out is not unset_value:
            return self.data_out
        self.data_out = self.data
        for output_filter in self.default_input_filters + self.output_filters:
            self.data_out = output_filter(self.data_out)
        return self.data_out
