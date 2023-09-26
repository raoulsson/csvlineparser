from __future__ import annotations

import logging

from csvlineparser.core.column_expander import ColumnExpander
from csvlineparser.core.exceptions import IllegalArgumentException

logger = logging.getLogger(__name__)


class CsvDataTypeMapping:
    """ Put this into a map with key being column name.
    If you clean up the key, use the original one.
    datatype will run validations and required will throw an exception if the column is empty.
    If ignored is true, the column will be removed. """

    def __init__(self, col_name: str,
                 data_type: str,
                 required: bool,
                 ignored: bool,
                 rename_to: str | None,
                 column_expander: ColumnExpander | None) -> None:
        super().__init__()
        if data_type not in ['double', 'int', 'boolean', 'string', 'datetime']:
            raise IllegalArgumentException(f'Currently not supported data type for CSV cleaning: {data_type}')
        self.__col_name = col_name
        self.__data_type = data_type
        self.__required = required
        self.__ignored = ignored
        self.__rename_to = rename_to
        self.__column_expander = column_expander

    def get_col_name(self) -> str:
        """ Returns the original name """
        return self.__col_name

    def get_type(self) -> str:
        """ currently only: double, int, boolean, string, datetime """
        return self.__data_type

    def is_required(self) -> bool:
        """ Will either a) throw an exception if isIgnored() is true, else b) log a warning """
        return self.__required

    def is_ignored(self) -> bool:
        return self.__ignored

    def get_rename_to(self) -> str | None:
        return self.__rename_to

    def get_column_expander(self) -> ColumnExpander | None:
        return self.__column_expander

    def __repr__(self) -> str:
        return f'col_name: {self.__col_name}, data_type: {self.__data_type}, required: {self.__required}, ' \
               f'ignored: {self.__ignored}, rename_to: {self.__rename_to}, ' \
               f'has_column_expander: {self.__column_expander is not None}'
