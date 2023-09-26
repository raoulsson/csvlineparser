from __future__ import annotations

import logging

from csvlineparser.clientutils.csv_console_consumer import CsvConsoleConsumer
from csvlineparser.core.csv_context_provider import CsvContextProvider

logger = logging.getLogger(__name__)


class CsvCleanerConsumer(CsvConsoleConsumer):

    def __init__(self, has_header: bool = True, csv_context_provider: CsvContextProvider | None = None) -> None:
        super().__init__()
        self.csv_context_provider = csv_context_provider
        if csv_context_provider:
            self.delimiter = csv_context_provider.get_delimiter()
        else:
            self.delimiter = ','
        self.has_header = has_header
        self.__line = ''
        self.__line_num = 0
        self.__col_count = 0
        self.__all_lines = []

    def consume_field(self, input_value: str) -> None:
        super().consume_field(input_value)

        # Ignored column?
        if self.csv_context_provider.is_column_ignored(self.__col_count):
            if self.__line_num == 0:
                logger.debug("Ignoring column " + str(self.__col_count) + ': ' + input_value)
            self.__col_count += 1
            return

        if self.csv_context_provider:
            if self.__line_num == 0:
                if self.has_header:
                    input_value = self.csv_context_provider.handle_header_element(input_value, self.__line_num,
                                                                                  self.__col_count)
                    if isinstance(input_value, list):
                        # self.__col_count += len(input_value) - 1
                        input_value = self.delimiter.join(input_value)
                else:
                    input_value = self.csv_context_provider.handle_data_element(input_value, self.__line_num,
                                                                                self.__col_count)
            else:
                input_value = self.csv_context_provider.handle_data_element(input_value, self.__line_num,
                                                                            self.__col_count)
                # self.__col_count += 0
                if isinstance(input_value, list):
                    self.__col_count += 1
                    for split_value in input_value:
                        self.__line += str(split_value) + self.delimiter
                    return

        self.__col_count += 1
        self.__line += str(input_value) + self.delimiter

    def signal_end_of_record(self) -> None:
        super().signal_end_of_record()
        self.__line = self.__line[:-1]
        self.__all_lines.append(self.__line)
        self.__line = ''
        self.__line_num += 1
        self.__col_count = 0

    def signal_end_of_line(self) -> None:
        super().signal_end_of_line()

    def get_header(self) -> str:
        return self.__all_lines[0]

    def get_data(self) -> list:
        return self.__all_lines[1:]

    def get_all(self) -> list:
        return self.__all_lines

    def get_line(self, line_num: int) -> str:
        return self.__all_lines[line_num]
