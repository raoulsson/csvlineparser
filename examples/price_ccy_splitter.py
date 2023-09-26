from __future__ import annotations

import logging
from typing import Union

from csvlineparser.core.field_splitter import FieldSplitter

logger = logging.getLogger(__name__)


class PriceCCYSplitter(FieldSplitter):

    def __init__(self, ) -> None:
        super().__init__()

    def split_single_value_to_many(self, original_value: str | bool | int | float | None) -> (
            list)[Union[str, bool, int, float, None]]:
        """ Transform a string like 'EUR100.00' to [100.00, 'EUR']. Also for negative numbers displayed as
        '−EUR100.00'. Also single quotes in numbers are removed. """
        original_value = original_value.replace('`', '')
        original_value = original_value.replace('', '')
        if not original_value:
            return [original_value]
        if not isinstance(original_value, str):

            return [original_value]
        if len(original_value) < 4:
            return [original_value]
        if original_value.startswith('−') or original_value.startswith('-'):
            if not original_value[1:4].isalpha():
                return [original_value]
            if not original_value[4:].replace('.', '').isdigit():
                return [original_value]
            return [float(original_value[4:]) * -1, str(original_value[1:4])]
        else:
            if not original_value[0:3].isalpha():
                return [original_value]
            if not original_value[3:].replace('.', '').isdigit():
                return [original_value]
            return [float(original_value[3:]), str(original_value[0:3])]
