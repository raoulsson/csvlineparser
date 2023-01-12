from __future__ import annotations

import logging

from src.csvlineparser.exceptions import IllegalArgumentException

logger = logging.getLogger(__name__)


class CsvDataTypeMapping:
    """ Put this into a map with key being column name.
    If you clean up the key, use the original one. """

    def __init__(self, colName: str, dataType: str, required: bool, ignored: bool) -> None:
        super().__init__()
        if dataType not in ['double', 'int', 'boolean', 'string', 'datetime']:
            raise IllegalArgumentException(f'Currently not supported data type for CSV cleaning: {dataType}')
        self.__colName = colName
        self.__dataType = dataType
        self.__required = required
        self.__ignored = ignored

    def getColName(self) -> str:
        """ Returns the name, for convenience, mostly debugging and choking up """
        return self.__colName

    def getType(self) -> str:
        """ currently only: double, int, boolean, string, datetime """
        return self.__dataType

    def isRequired(self) -> bool:
        """ Will either a) throw an exception if isIgnored() is true, else b) log a warning """
        return self.__required

    def isIgnored(self) -> bool:
        return self.__ignored

    def __repr__(self) -> str:
        return
