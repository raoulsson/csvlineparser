from __future__ import annotations

import logging

from src.csvlineparser.exceptions import IllegalArgumentException

logger = logging.getLogger(__name__)


class CsvDataTypeMapping:
    """ Put this into a map with key being column name.
    If you clean up the key, use the original one. """

    def __init__(self, col_name: str, data_type: str, required: bool, ignored: bool) -> None:
        super().__init__()
        if data_type not in ['double', 'int', 'boolean', 'string', 'datetime']:
            raise IllegalArgumentException(f'Currently not supported data type for CSV cleaning: {data_type}')
        self.__col_name = col_name
        self.__data_type = data_type
        self.__required = required
        self.__ignored = ignored

    def get_col_name(self) -> str:
        """ Returns the name, for convenience, mostly debugging and choking up """
        return self.__col_name

    def get_type(self) -> str:
        """ currently only: double, int, boolean, string, datetime """
        return self.__data_type

    def is_required(self) -> bool:
        """ Will either a) throw an exception if isIgnored() is true, else b) log a warning """
        return self.__required

    def is_ignored(self) -> bool:
        return self.__ignored

    def __repr__(self) -> str:
        return 'n/a'
