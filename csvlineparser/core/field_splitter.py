from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Union

logger = logging.getLogger(__name__)


class FieldSplitter(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def split_single_value_to_many(self, original_value: str | bool | int | float | None) -> (
            list)[Union[str, bool, int, float, None]]:
        pass
