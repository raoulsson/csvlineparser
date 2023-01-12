from __future__ import annotations

import logging

from csvlineparser.csv_consumer_interface import ICsvConsumer
from csvlineparser.exceptions import IllegalStateException

logger = logging.getLogger(__name__)


class MultiConsumer(ICsvConsumer):

    def __init__(self, fail_fast: bool = False) -> None:
        """ ICsvConsumer can be appended, and it will delegate the call to many.
        If failFast, will raise an exception data columns differ from header columns
        (or generally the first column) """
        super().__init__()
        self.__header_read: bool = False
        self.__header_elem_count = 0
        self.__line_elem_count = 0
        self.__consumers: list[ICsvConsumer] = []
        self.__fail_fast: bool = fail_fast
        self.__line_num = 1

    def addConsumers(self, consumer: ICsvConsumer | list[ICsvConsumer]) -> None:
        if isinstance(consumer, list):
            self.__consumers.extend(consumer)
        else:
            self.__consumers.append(consumer)

    def consume_field(self, s: str) -> None:
        if not self.__header_read:
            self.__header_elem_count += 1
        else:
            self.__line_elem_count += 1
        for consumer in self.__consumers:
            consumer.consume_field(s)

    def signal_end_of_record(self) -> None:
        if self.__header_read:
            if self.__header_elem_count != self.__line_elem_count:
                if self.__fail_fast:
                    raise IllegalStateException(f'Header element count [{self.__header_elem_count}] does not '
                                    f'match line element count [{self.__line_elem_count}]. '
                                    f'Line: {self.__line_num}')
        self.__header_read = True
        self.__line_elem_count = 0
        self.__line_num += 1
        for consumer in self.__consumers:
            consumer.signal_end_of_record()

    def signal_end_of_line(self) -> None:
        for consumer in self.__consumers:
            consumer.signal_end_of_line()
