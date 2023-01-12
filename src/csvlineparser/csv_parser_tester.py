import logging

from src.csvlineparser.csv_consumer_interface import ICsvConsumer

logger = logging.getLogger(__name__)


class CsvConsumerTester(ICsvConsumer):

    def __init__(self, expectedFields: list[str]) -> None:
        super().__init__()
        self.expectedFields: list[str] = expectedFields
        self.fieldIndex: int = 0

    def consumeField(self, s: str) -> None:
        if self.expectedFields[self.fieldIndex] != s:
            raise Exception(f'field [{self.expectedFields[self.fieldIndex]}] expected, but [{s}] returned')
        self.fieldIndex += 1

    def signalEndOfRecord(self) -> None:
        if self.expectedFields[self.fieldIndex] != 'EOR':
            self.fieldIndex += 1
            raise Exception('End of record signalled but not expected')

    def signalEndOfFile(self) -> None:
        if self.expectedFields[self.fieldIndex] != '':
            self.fieldIndex += 1
            raise Exception('End of file signalled but not expected')
