from __future__ import annotations

import logging

from src.csvlineparser.char_tokenizer_interface import ICharTokenizer
from src.csvlineparser.csv_consumer_interface import ICsvConsumer
from src.csvlineparser.exceptions import CsvParserTooMuchDataException, CsvParserNoTermQuoteException
from src.csvlineparser.multi_consumer import MultiConsumer

logger = logging.getLogger(__name__)


class CsvParser:

    def __init__(self, debugOffset: int = 20) -> None:
        super().__init__()
        self.__firstRow: bool = True
        self.__currentRow: str = ''
        self.__debugOffset: int = debugOffset
        self.__lineNumber: int = 0

    def parse(self, reader: ICharTokenizer,
              consumers: ICsvConsumer | list[ICsvConsumer],
              failFast: bool = True) -> None:
        multiConsumer = MultiConsumer(failFast=failFast)
        multiConsumer.addConsumers(consumers)
        self.__parseCsvFile(reader, multiConsumer)

    def __parseCsvFile(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        while reader.peek() != 'EOF':
            self.__parseCsvRecord(reader, consumer)
        consumer.signalEndOfFile()

    def __parseCsvRecord(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        self.__lineNumber += 1
        self.__parseCsvStringList(reader, consumer)
        ch: str = reader.read()
        if ch == 'EOF':
            reader.unread(ch)
            ch = '\n'
        if ch != '\n':
            raise CsvParserTooMuchDataException(f'End of record was expected but more data exists: >{ch}<',
                                                reader.getPos(), reader.getSegment(reader.getPos()
                                                                                   - self.__debugOffset,
                                                                                   self.__debugOffset * 2),
                                                self.__debugOffset, self.__lineNumber)
        consumer.signalEndOfRecord()

    def __parseCsvStringList(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        ch: str
        while True:
            self.__parseRawString(reader, consumer)
            ch = reader.read()
            if ch != ',':
                break
        reader.unread(ch)

    def __isFieldTerminator(self, c: str) -> bool:
        return c == ',' or c == '\n' or c == 'EOF'

    def __isSpace(self, c: str) -> bool:
        return c == ' ' or c == '\t'

    def __parseOptionalSpaces(self, reader: ICharTokenizer) -> None:
        ch: str
        while True:
            ch = reader.read()
            if not self.__isSpace(ch):
                break
        reader.unread(ch)

    def __parseRawString(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        self.__parseOptionalSpaces(reader)
        self.__parseRawField(reader, consumer)
        if not self.__isFieldTerminator(reader.peek()):
            self.__parseOptionalSpaces(reader)

    def __parseRawField(self, reader: ICharTokenizer, consumer: ICsvConsumer) -> None:
        fieldValue: str = ''

        ch: str = reader.peek()
        if not self.__isFieldTerminator(ch):
            if ch == '"':
                fieldValue = self.__parseQuotedField(reader)
            else:
                fieldValue = self.__parseSimpleField(reader)
        consumer.consumeField(fieldValue.strip())

    def __parseQuotedField(self, reader: ICharTokenizer) -> str:
        reader.read()  # read and discard initial quote

        field: str = self.__parseEscapedField(reader)

        ch: str = reader.read()
        if ch != '"':
            reader.unread(ch)
            raise CsvParserNoTermQuoteException('Quoted field has no terminating double quote')
        return field

    def __parseEscapedField(self, reader: ICharTokenizer) -> str:
        sb: list[str] = list()

        self.__parseSubField(reader, sb)
        ch: str = reader.read()
        while self.__processDoubleQuote(reader, ch):
            sb.append('"')
            self.__parseSubField(reader, sb)
            ch = reader.read()
        reader.unread(ch)

        return ''.join(sb)

    def __parseSubField(self, reader: ICharTokenizer, sb: list[str]) -> None:
        ch: str = reader.read()
        while ch != '"' and ch != 'EOF':
            sb.append(ch)
            ch = reader.read()
        reader.unread(ch)

    def __isBadSimpleFieldChar(self, c: str) -> bool:
        return self.__isFieldTerminator(c) or c == '"'

    def __parseSimpleField(self, reader: ICharTokenizer) -> str:
        ch: str = reader.read()
        if self.__isBadSimpleFieldChar(ch) or self.__isSpace(ch):
            reader.unread(ch)
            return ''

        sb: list[str] = list()
        sb.append(ch)
        ch = reader.read()
        while not self.__isBadSimpleFieldChar(ch):
            sb.append(ch)
            ch = reader.read()
        reader.unread(ch)
        return ''.join(sb)

    def __processDoubleQuote(self, reader: ICharTokenizer, ch: str) -> bool:
        if ch == '"' and reader.peek() == '"':
            reader.read()  # discard second quote of double
            return True
        return False
