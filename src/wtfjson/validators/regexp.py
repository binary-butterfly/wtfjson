# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

import re
from typing import Any, Optional, Union, Pattern, Match, TYPE_CHECKING

from ..fields import Field
from ..validators import Validator
from ..exceptions import ValidationError

if TYPE_CHECKING:
    from ..dict_input import DictInput
    from ..list_input import ListInput


class Regexp(Validator):
    rule: Pattern
    default_message = 'regexp failed'

    def __init__(self, rule: Union[str, Pattern], flags: int = 0, message: Optional[str] = None):
        super().__init__(message)
        self.rule = rule if type(rule) is Pattern else re.compile(rule, flags)

    def __call__(self, value: Any, form: Union['DictInput', 'ListInput'], field: Field) -> Match:
        match = self.rule.match(value)
        if match is None:
            raise ValidationError(self.message)
        return match
