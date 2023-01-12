from __future__ import annotations

import logging

from src.csvlineparser.csv_console_consumer import CsvConsoleConsumer
from src.csvlineparser.csv_context_provider import CsvContextProvider

logger = logging.getLogger(__name__)


class CsvCleanerConsumer(CsvConsoleConsumer):

    def __init__(self, hasHeader: bool = True, csvContextProvider: CsvContextProvider | None = None) -> None:
        super().__init__()
        self.csvContextProvider = csvContextProvider
        if csvContextProvider:
            self.delimiter = csvContextProvider.getDelimiter()
        else:
            self.delimiter = ','
        self.hasHeader = hasHeader
        self.__line = ''
        self.__lineNum = 0
        self.__colCount = 0
        self.__allLines = []

    def consumeField(self, inputValue: str) -> None:
        super().consumeField(inputValue)

        if self.csvContextProvider:
            if self.__lineNum == 0:
                if self.hasHeader:
                    inputValue = self.csvContextProvider.handleHeaderElement(inputValue, self.__lineNum,
                                                                             self.__colCount)
                else:
                    inputValue = self.csvContextProvider.handleDataElement(inputValue, self.__lineNum, self.__colCount)
            else:
                inputValue = self.csvContextProvider.handleDataElement(inputValue, self.__lineNum, self.__colCount)

        self.__line += inputValue + self.delimiter
        self.__colCount += 1

    def signalEndOfRecord(self) -> None:
        super().signalEndOfRecord()
        self.__line = self.__line[:-1]
        self.__allLines.append(self.__line)
        self.__line = ''
        self.__lineNum += 1
        self.__colCount = 0

    def signalEndOfFile(self) -> None:
        super().signalEndOfFile()

    def getHeader(self) -> str:
        return self.__allLines[0]

    def getData(self) -> list:
        return self.__allLines[1:]

    def getAll(self) -> list:
        return self.__allLines

    def getLine(self, lineNum: int) -> str:
        return self.__allLines[lineNum]
