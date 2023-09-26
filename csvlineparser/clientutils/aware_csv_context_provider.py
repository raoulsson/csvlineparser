from __future__ import annotations

import datetime
import logging

from csvlineparser.core.csv_context_provider import CsvContextProvider
from csvlineparser.core.csv_data_type_mapping import CsvDataTypeMapping

logger = logging.getLogger(__name__)


class AwareCsvContextProvider(CsvContextProvider):

    def __init__(self, data_type_mappings: dict[int, CsvDataTypeMapping] | None, aws_compatible: bool) -> None:
        super().__init__()
        self.__refData: dict[int, CsvDataTypeMapping] | None = data_type_mappings
        self.__aws_compatible = aws_compatible

    def get_delimiter(self) -> str:
        """ Returns the char used to delimit columns. Defaults to comma (,) """
        return ','

    def handle_header_element(self, input_value: str, row: int, column: int) -> list[str] | str:
        """ Apply transformations to the in value, which is a header cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        if self.__refData[column].get_column_expander() is not None:
            logger.debug('Expanding column ' + str(column) + ': ' + input_value + ' to '
                  + str(self.__refData[column].get_column_expander().get_column_names()))

            collector = []
            for column_name in self.__refData[column].get_column_expander().get_column_names():
                if self.__aws_compatible and '.' in input_value:
                    column_name = column_name.replace('.', '_')
                if not (column_name.startswith('"') and column_name.endswith('"')):
                    column_name = f'"{column_name}"'
                collector.append(column_name)
            return collector

        elif self.__refData[column].get_rename_to() is not None:
            logger.debug('Renaming column ' + str(column) + ': ' + input_value + ' to ' + str(
                self.__refData[column].get_rename_to()))
            input_value = str(self.__refData[column].get_rename_to())

        # header for glue cannot have dots in AWS 2022 (.)
        if self.__aws_compatible and '.' in input_value:
            input_value = input_value.replace('.', '_')
        if not (input_value.startswith('"') and input_value.endswith('"')):
            input_value = f'"{input_value}"'
        return input_value

    def handle_data_element(self, input_value: str, row: int, column: int) -> list[str] | str:
        """ Apply transformations to the in value, which is a data cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        if self.__refData[column].is_ignored():
            return input_value

        if self.__refData[column].get_column_expander() is not None:
            collector = []
            for split_input_value in self.__refData[column].get_column_expander().split_single_value_to_many(
                    input_value):
                collector.append(split_input_value)
            logger.debug('Expanded values in column ' + str(column) + ': From ' + input_value + ' to ' + str(collector))
            return collector

        input_value = self.check_for_empty(column, input_value)
        input_value = self.check_type(column, input_value)

        return input_value

    def check_for_empty(self, column, input_value):
        if isinstance(input_value, str) and input_value != '':
            if input_value.lower() == 'true' or input_value.lower() == 'false':
                input_value = input_value.lower()
            if '"' in input_value:
                input_value = input_value.replace('"', '""')
            if self.__toDate(input_value) is not None:
                input_value = self.__toDate(input_value)
            elif (self.get_delimiter() in input_value or ' ' in input_value
                  or self.__refData[column].get_type() == 'string'):
                input_value = f'"{input_value}"'
        else:
            if self.__refData[column].get_type() == 'string':
                input_value = '""'
            else:
                input_value = ''
        return input_value

    def check_type(self, column, input_value):
        if self.__refData:
            expected_data_type = self.__refData[column].get_type()
            if input_value == '' and self.__refData[column].is_required():
                if expected_data_type == 'double':
                    logger.warning(f'Empty double found in column: {self.__refData[column].get_col_name()}. '
                                   f'Replacing with 0.0')
                    input_value = '0.0'
                elif expected_data_type == 'int':
                    logger.warning(f'Empty int found in column: {self.__refData[column].get_col_name()}. '
                                   f'Replacing with 0')
                    input_value = '0'
                elif expected_data_type == 'boolean':
                    logger.warning(f'Empty boolean found in column: {self.__refData[column].get_col_name()}. '
                                   f'Replacing with False')
                    input_value = 'false'
                elif expected_data_type == 'datetime':
                    raise ValueError(
                        f'Empty date datetime found for column: {self.__refData[column].get_col_name()}')
                    # logger.warning(f'Empty date datetime found for column: {self.refData[self.rowCount].name}')
                elif expected_data_type == 'string':
                    logger.info(f'Skipping: Empty string: {self.__refData[column].get_col_name()}, '
                                f'expected type: {expected_data_type}')
                else:
                    raise ValueError(f'Empty value found for column: {self.__refData[column].get_col_name()} '
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

    def is_column_ignored(self, column):
        if self.__refData is not None:
            return self.__refData[column].is_ignored()
        return False
