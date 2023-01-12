import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CsvContextProvider(ABC):

    def __init__(self) -> None:
        super().__init__()

    def get_delimiter(self) -> str:
        """ Returns the char used to delimit columns. Defaults to comma (,) """
        return ','

    @abstractmethod
    def handle_header_element(self, input_value: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a header cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        pass

    @abstractmethod
    def handle_data_element(self, input_value: str, row: int, column: int) -> str:
        """ Apply transformations to the input value, which is a data cell.
        The row and column parameters are there if you need it. Return value
        will be inserted into resulting CSV object """
        pass
