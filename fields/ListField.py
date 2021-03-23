# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from copy import deepcopy
from typing import Optional, Any, List
from fields import Field
from validators import Type, ListLength
from util import unset_value


class ListField(Field):
    entries: List[Field] = unset_value

    def __init__(self, unbound_field: Field, min_entries: Optional[int] = 0, max_entries: Optional[int] = None):
        super().__init__()
        assert min_entries >= 0
        assert max_entries is None or max_entries >= min_entries
        self.default_validators = [
            Type(data_type=list),
            ListLength(min_entries, max_entries)
        ]
        self.unbound_field = unbound_field

    def process_in(self, data_raw: Any):
        super().process_in(data_raw)
        if type(self._data) is not list:
            return
        self.entries = []
        for item in data_raw:
            entry = deepcopy(self.unbound_field)
            entry.init_form(self._form, '%s.%s' % (self._field_name, len(self.entries)))
            entry.process_in(item)
            self.entries.append(entry)

    def validate(self) -> bool:
        super().validate()
        if self.entries is unset_value:
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
