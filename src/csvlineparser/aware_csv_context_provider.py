from __future__ import annotations

import datetime
import logging

from src.csvlineparser.csv_context_provider import CsvContextProvider
from src.csvlineparser.csv_data_type_mapping import CsvDataTypeMapping

logger = logging.getLogger(__name__)


class AwareCsvContextProvider(CsvContextProvider):

    def __init__(self, dataTypeMappings: dict[int, CsvDataTypeMapping] | None) -> None:
        super().__init__()
        self.__lineNum: int = 0
        self.__colCount: int = 0
        self.__refData: dict[int, CsvDataTypeMapping] | None = dataTypeMappings

    def getDelimiter(self) -> str:
        """ Returns the char used to delimit columns. Defaults to comma (,) """
        return ','

    def handleHeaderElement(self, inputValue: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a header cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        # header for glue cannot have dots (.)
        if '.' in inputValue:
            inputValue = inputValue.replace('.', '_')
        return inputValue

    def handleDataElement(self, inputValue: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a data cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        if self.__lineNum == 0:
            if '.' in inputValue:
                inputValue = inputValue.replace('.', '_')
        if inputValue != '':
            if inputValue.lower() == 'true' or inputValue.lower() == 'false':
                inputValue = inputValue.lower()
            if '"' in inputValue:
                inputValue = inputValue.replace('"', '""')
            if self.__toDate(inputValue) is not None:
                inputValue = self.__toDate(inputValue)
            elif self.getDelimiter() in inputValue:
                inputValue = f'"{inputValue}"'
        else:
            inputValue = ''

        if self.__refData:
            expectedDataType = self.__refData[self.__colCount].getType()
            if inputValue == '' and self.__refData[self.__colCount].isRequired():
                if expectedDataType == 'double':
                    logger.warning(f'Empty double found in column: {self.__refData[self.__colCount].getColName()}. '
                                   f'Replacing with 0.0')
                    inputValue = '0.0'
                elif expectedDataType == 'int':
                    logger.warning(f'Empty int found in column: {self.__refData[self.__colCount].getColName()}. '
                                   f'Replacing with 0')
                    inputValue = '0'
                elif expectedDataType == 'boolean':
                    logger.warning(f'Empty boolean found in column: {self.__refData[self.__colCount].getColName()}. '
                                   f'Replacing with False')
                    inputValue = 'false'
                elif expectedDataType == 'datetime':
                    raise ValueError(
                        f'Empty date datetime found for column: {self.__refData[self.__colCount].getColName()}')
                    # logger.warning(f'Empty date datetime found for column: {self.refData[self.rowCount].name}')
                elif expectedDataType == 'string':
                    logger.info(f'Skipping: Empty string: {self.__refData[self.__colCount].getColName()}, '
                                f'expected type: {expectedDataType}')
                else:
                    raise ValueError(f'Empty value found for column: {self.__refData[self.__colCount].getColName()} '
                                     f'and type: {expectedDataType}')
        return inputValue

    def __toDate(self, s: str) -> str | None:
        """ Check if string should be a date of format: YYYY-MM-DD or YYYY-MM-DD hh:mm:ss """
        try:
            return datetime.datetime.strptime(s, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        return None
