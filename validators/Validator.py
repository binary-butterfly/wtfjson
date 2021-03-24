# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from typing import Optional, Any
from abc import ABC, abstractmethod
from fields import Field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import Form


class Validator(ABC):
    default_message = 'common error'

    def __init__(self, message: Optional[str] = None):
        self.message = message if message is not None else self.default_message

    @abstractmethod
    def __call__(self, value: Any, form: 'Form', field: Field) -> None:
        pass


