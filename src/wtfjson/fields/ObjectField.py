# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Any, TYPE_CHECKING
from ..fields import Field
from ..validators import Type
from ..util import unset_value
if TYPE_CHECKING:
    from ..DictInput import DictInput


class ObjectField(Field):
    _obj: 'DictInput' = unset_value
    pre_validators = [
        Type(data_type=dict)
    ]

    def __init__(self, form_class: 'DictInput', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = form_class

    def process_in(self, data_raw: Any):
        super().process_in(data_raw)
        if self.validation_stopped:
            return
        self._obj = self.form_class(data_raw)

    def validate(self) -> bool:
        super().validate()
        if self._obj is unset_value or self.validation_stopped:
            return not self.has_errors
        self._obj.validate()
        self._errors.update({'%s.%s' % (self._field_name, path): error for path, error in self._obj.errors.items()})
        return not self.has_errors

    @property
    def data(self):
        return unset_value if self._obj is unset_value else self._obj.data

    @property
    def out(self):
        return unset_value if self._obj is unset_value else self._obj.out
