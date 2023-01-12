from __future__ import annotations

import logging

from src.csvlineparser.csv_consumer_interface import ICsvConsumer

logger = logging.getLogger(__name__)


class MultiConsumer(ICsvConsumer):

    def __init__(self, failFast: bool = False) -> None:
        """ ICsvConsumer can be appended, and it will delegate the call to many.
        If failFast, will raise an exception data columns differ from header columns
        (or generally the first column) """
        super().__init__()
        self.__headerRead: bool = False
        self.__headerElemCount = 0
        self.__lineElemCount = 0
        self.__consumers: list[ICsvConsumer] = []
        self.__failFast: bool = failFast
        self.__lineNum = 1

    def addConsumers(self, consumer: ICsvConsumer | list[ICsvConsumer]) -> None:
        if isinstance(consumer, list):
            self.__consumers.extend(consumer)
        else:
            self.__consumers.append(consumer)

    def consumeField(self, s: str) -> None:
        if not self.__headerRead:
            self.__headerElemCount += 1
        else:
            self.__lineElemCount += 1
        for consumer in self.__consumers:
            consumer.consumeField(s)

    def signalEndOfRecord(self) -> None:
        if self.__headerRead:
            if self.__headerElemCount != self.__lineElemCount:
                if self.__failFast:
                    raise Exception(f'Header element count [{self.__headerElemCount}] does not '
                                    f'match line element count [{self.__lineElemCount}]. '
                                    f'Line: {self.__lineNum}')
        self.__headerRead = True
        self.__lineElemCount = 0
        self.__lineNum += 1
        for consumer in self.__consumers:
            consumer.signalEndOfRecord()

    def signalEndOfFile(self) -> None:
        for consumer in self.__consumers:
            consumer.signalEndOfFile()
