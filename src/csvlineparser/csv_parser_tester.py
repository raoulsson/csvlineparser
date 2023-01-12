import logging

from src.csvlineparser.csv_consumer_interface import ICsvConsumer
from src.csvlineparser.exceptions import IllegalStateException

logger = logging.getLogger(__name__)


class CsvConsumerTester(ICsvConsumer):

    def __init__(self, expected_fields: list[str]) -> None:
        super().__init__()
        self.expected_fields: list[str] = expected_fields
        self.field_index: int = 0

    def consume_field(self, s: str) -> None:
        if self.expected_fields[self.field_index] != s:
            raise IllegalStateException(f'field [{self.expected_fields[self.field_index]}] expected, but [{s}] returned')
        self.field_index += 1

    def signal_end_of_record(self) -> None:
        if self.expected_fields[self.field_index] != 'EOR':
            self.field_index += 1
            raise IllegalStateException('End of record signalled but not expected')

    def signal_end_of_line(self) -> None:
        if self.expected_fields[self.field_index] != '':
            self.field_index += 1
            raise IllegalStateException('End of file signalled but not expected')
