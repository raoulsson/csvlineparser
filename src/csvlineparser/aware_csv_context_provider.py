from __future__ import annotations

import datetime
import logging

from src.csvlineparser.csv_context_provider import CsvContextProvider
from src.csvlineparser.csv_data_type_mapping import CsvDataTypeMapping

logger = logging.getLogger(__name__)


class AwareCsvContextProvider(CsvContextProvider):

    def __init__(self, data_type_mappings: dict[int, CsvDataTypeMapping] | None) -> None:
        super().__init__()
        self.__lineNum: int = 0
        self.__colCount: int = 0
        self.__refData: dict[int, CsvDataTypeMapping] | None = data_type_mappings

    def get_delimiter(self) -> str:
        """ Returns the char used to delimit columns. Defaults to comma (,) """
        return ','

    def handle_header_element(self, input_value: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a header cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        # header for glue cannot have dots (.)
        if '.' in input_value:
            input_value = input_value.replace('.', '_')
        return input_value

    def handle_data_element(self, input_value: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a data cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        if self.__lineNum == 0 and '.' in input_value:
                input_value = input_value.replace('.', '_')
        if input_value != '':
            if input_value.lower() == 'true' or input_value.lower() == 'false':
                input_value = input_value.lower()
            if '"' in input_value:
                input_value = input_value.replace('"', '""')
            if self.__toDate(input_value) is not None:
                input_value = self.__toDate(input_value)
            elif self.get_delimiter() in input_value:
                input_value = f'"{input_value}"'
        else:
            input_value = ''

        if self.__refData:
            expected_data_type = self.__refData[self.__colCount].get_type()
            if input_value == '' and self.__refData[self.__colCount].is_required():
                if expected_data_type == 'double':
                    logger.warning(f'Empty double found in column: {self.__refData[self.__colCount].get_col_name()}. '
                                   f'Replacing with 0.0')
                    input_value = '0.0'
                elif expected_data_type == 'int':
                    logger.warning(f'Empty int found in column: {self.__refData[self.__colCount].get_col_name()}. '
                                   f'Replacing with 0')
                    input_value = '0'
                elif expected_data_type == 'boolean':
                    logger.warning(f'Empty boolean found in column: {self.__refData[self.__colCount].get_col_name()}. '
                                   f'Replacing with False')
                    input_value = 'false'
                elif expected_data_type == 'datetime':
                    raise ValueError(
                        f'Empty date datetime found for column: {self.__refData[self.__colCount].get_col_name()}')
                    # logger.warning(f'Empty date datetime found for column: {self.refData[self.rowCount].name}')
                elif expected_data_type == 'string':
                    logger.info(f'Skipping: Empty string: {self.__refData[self.__colCount].get_col_name()}, '
                                f'expected type: {expected_data_type}')
                else:
                    raise ValueError(f'Empty value found for column: {self.__refData[self.__colCount].get_col_name()} '
                                     f'and type: {expected_data_type}')
        return input_value

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
