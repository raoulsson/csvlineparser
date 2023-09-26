from __future__ import annotations

import logging
from typing import Union

from csvlineparser.core.field_splitter import FieldSplitter

logger = logging.getLogger(__name__)


class YearMonthDaySplitter(FieldSplitter):
    """
    Here we split a date like '2023-01-01T20:42:16.957+01:00' into 4 columns: original, year, month, day. See
    examples/example_parser.py for usage and the way the new columns are defined.
    """

    def __init__(self, ) -> None:
        super().__init__()

    def split_single_value_to_many(self, original_value: str | bool | int | float | None) -> (
            list)[Union[str, bool, int, float, None]]:
        """ Transform a string like '2023-01-01T20:42:16.957+01:00' to [original, 2020, 1, 1]. """
        if not original_value:
            return [original_value]
        if not isinstance(original_value, str):
            return [original_value]
        if len(original_value) < 10:
            return [original_value]
        if not original_value[0:4].isdigit():
            return [original_value]
        if not original_value[5:7].isdigit():
            return [original_value]
        if not original_value[8:10].isdigit():
            return [original_value]
        return [original_value, int(original_value[0:4]), int(original_value[5:7]), int(original_value[8:10])]
