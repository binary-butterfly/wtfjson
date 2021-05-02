# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Optional, Any, List

from .Field import FieldState
from ..fields import Field, UnboundField
from ..validators import Type, ListLength
from ..util import unset_value


class ListField(Field):
    entries: List[Field] = unset_value

    def __init__(self,
                 unbound_field: UnboundField,
                 min_entries: Optional[int] = 0,
                 max_entries: Optional[int] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        assert min_entries >= 0
        assert max_entries is None or max_entries >= min_entries
        self.pre_validators = [
            Type(data_type=list),
            ListLength(min_entries, max_entries)
        ]
        self.unbound_field = unbound_field

    def process_in(self, data_raw: Any):
        super().process_in(data_raw)
        if self.validation_stopped:
            return 
        self.entries = []
        for item in self.data_processed:
            entry = self.unbound_field.bind(self._form, '%s.%s' % (self._field_name, len(self.entries)))
            entry.process_in(item)
            self.entries.append(entry)

    def validate(self) -> bool:
        super().validate()
        if self.data_processed is unset_value and not self.required:
            self.state = FieldState.validated
            return not self.has_errors
        if self.validation_stopped:
            return not self.has_errors
        for entry in self.entries:
            entry.validate()
            self._errors.update(entry.errors)
        return not self.has_errors

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    @property
    def data(self):
        return unset_value if self.entries is unset_value else [f.data for f in self.entries]

    @property
    def out(self):
        return unset_value if self.entries is unset_value else [f.out for f in self.entries]
