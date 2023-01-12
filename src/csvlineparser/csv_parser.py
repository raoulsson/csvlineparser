from __future__ import annotations

import logging

from csvlineparser.char_tokenizer_interface import ICharTokenizer
from csvlineparser.csv_consumer_interface import ICsvConsumer
from csvlineparser.exceptions import CsvParserTooMuchDataException, CsvParserNoTermQuoteException
from csvlineparser.multi_consumer import MultiConsumer

logger = logging.getLogger(__name__)


class CsvParser:

    def __init__(self, debug_offset: int = 20) -> None:
        super().__init__()
        self.__first_row: bool = True
        self.__current_row: str = ''
        self.__debug_offset: int = debug_offset
        self.__line_number: int = 0

    def parse(self, reader: ICharTokenizer,
              consumers: ICsvConsumer | list[ICsvConsumer],
              fail_fast: bool = True) -> None:
        multi_consumer = MultiConsumer(fail_fast=fail_fast)
        multi_consumer.addConsumers(consumers)
        self.__parse_csv_file(reader, multi_consumer)

    def __parse_csv_file(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        while reader.peek() != 'EOF':
            self.__parse_csv_record(reader, consumer)
        consumer.signal_end_of_line()

    def __parse_csv_record(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        self.__line_number += 1
        self.__parse_csv_string_list(reader, consumer)
        ch: str = reader.read()
        if ch == 'EOF':
            reader.unread(ch)
            ch = '\n'
        if ch != '\n':
            raise CsvParserTooMuchDataException(f'End of record was expected but more data exists: >{ch}<',
                                                reader.get_pos(), reader.get_segment(reader.get_pos()
                                                                                     - self.__debug_offset,
                                                                                     self.__debug_offset * 2),
                                                self.__debug_offset, self.__line_number)
        consumer.signal_end_of_record()

    def __parse_csv_string_list(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        ch: str
        while True:
            self.__parse_raw_string(reader, consumer)
            ch = reader.read()
            if ch != ',':
                break
        reader.unread(ch)

    def __is_field_terminator(self, c: str) -> bool:
        return c == ',' or c == '\n' or c == 'EOF'

    def __is_space(self, c: str) -> bool:
        return c == ' ' or c == '\t'

    def __parse_optional_space(self, reader: ICharTokenizer) -> None:
        ch: str
        while True:
            ch = reader.read()
            if not self.__is_space(ch):
                break
        reader.unread(ch)

    def __parse_raw_string(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        self.__parse_optional_space(reader)
        self.__parse_raw_field(reader, consumer)
        if not self.__is_field_terminator(reader.peek()):
            self.__parse_optional_space(reader)

    def __parse_raw_field(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        field_value: str = ''

        ch: str = reader.peek()
        if not self.__is_field_terminator(ch):
            if ch == '"':
                field_value = self.__parse_quoted_field(reader)
            else:
                field_value = self.__parse_simple_field(reader)
        consumer.consume_field(field_value.strip())

    def __parse_quoted_field(self, reader: ICharTokenizer) -> str:
        reader.read()  # read and discard initial quote

        field: str = self.__parse_escaped_field(reader)

        ch: str = reader.read()
        if ch != '"':
            reader.unread(ch)
            raise CsvParserNoTermQuoteException('Quoted field has no terminating double quote')
        return field

    def __parse_escaped_field(self, reader: ICharTokenizer) -> str:
        sb: list[str] = list()

        self.__parse_sub_field(reader, sb)
        ch: str = reader.read()
        while self.__process_double_quote(reader, ch):
            sb.append('"')
            self.__parse_sub_field(reader, sb)
            ch = reader.read()
        reader.unread(ch)

        return ''.join(sb)

    def __parse_sub_field(self, reader: ICharTokenizer, sb: list[str]) -> None:
        ch: str = reader.read()
        while ch != '"' and ch != 'EOF':
            sb.append(ch)
            ch = reader.read()
        reader.unread(ch)

    def __is_bad_simple_field_char(self, c: str) -> bool:
        return self.__is_field_terminator(c) or c == '"'

    def __parse_simple_field(self, reader: ICharTokenizer) -> str:
        ch: str = reader.read()
        if self.__is_bad_simple_field_char(ch) or self.__is_space(ch):
            reader.unread(ch)
            return ''

        sb: list[str] = list()
        sb.append(ch)
        ch = reader.read()
        while not self.__is_bad_simple_field_char(ch):
            sb.append(ch)
            ch = reader.read()
        reader.unread(ch)
        return ''.join(sb)

    def __process_double_quote(self, reader: ICharTokenizer, ch: str) -> bool:
        if ch == '"' and reader.peek() == '"':
            reader.read()  # discard second quote of double
            return True
        return False
