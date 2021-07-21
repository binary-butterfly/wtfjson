# encoding: utf-8

"""
binary butterfly validator
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Union, TYPE_CHECKING

from ..fields import Field

if TYPE_CHECKING:
    from ..dict_input import DictInput
    from ..list_input import ListInput


class Validator(ABC):
    default_message = 'common error'

    def __init__(self, message: Optional[str] = None):
        self.message = message if message is not None else self.default_message

    @abstractmethod
    def __call__(self, value: Any, parent: Union['DictInput', 'ListInput'], field: Field) -> None:
        pass
