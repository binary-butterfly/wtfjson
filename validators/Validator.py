# encoding: utf-8

"""
binary butterfly common
Copyright (c) 2017 - 2021, binary butterfly GmbH
All rights reserved.
"""

from typing import Optional
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
    def __call__(self, form: 'Form', field: Field) -> None:
        pass


