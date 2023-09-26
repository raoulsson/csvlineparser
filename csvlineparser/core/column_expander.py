from __future__ import annotations

import logging
from typing import Union

from csvlineparser.core.field_splitter import FieldSplitter

logger = logging.getLogger(__name__)


class ColumnExpander:

    def __init__(self, new_columns: list[str], field_splitter: FieldSplitter) -> None:
        self.__new_columns = new_columns
        self.__field_splitter = field_splitter

    def get_column_names(self) -> list[str]:
        return self.__new_columns

    def get_column_name_by_index(self, index: int) -> str:
        return self.__new_columns[index]

    def split_single_value_to_many(self, original_value: str | bool | int | float | None) -> (
            list)[Union[str, bool, int, float, None]]:
        return self.__field_splitter.split_single_value_to_many(original_value)
