import logging

from csvlineparser.csv_consumer_interface import ICsvConsumer

logger = logging.getLogger(__name__)


class CsvConsoleConsumer(ICsvConsumer):

    def __init__(self) -> None:
        super().__init__()
        self.__colIndex = 0
        self.__rowIndex = 0
        self.__num_cols = 0
        self.__num_rows = 0
        self.__matrix = {}

    def consume_field(self, s: str) -> None:
        self.__matrix[self.__colIndex, self.__rowIndex] = s
        self.__colIndex += 1
        if self.__num_cols < self.__colIndex:
            self.__num_cols += 1

    def signal_end_of_record(self) -> None:
        self.__rowIndex += 1
        self.__num_rows += 1
        self.__colIndex = 0

    def signal_end_of_line(self) -> None:
        print(f'End of file reached. Got {self.__num_cols} columns and {self.__num_rows} rows')

    def get_matrix(self) -> dict:
        return self.__matrix

    def get_column(self, col_index: int) -> list:
        col = []
        for i in range(0, self.__num_rows):
            col.append(self.__matrix[col_index, i])
        return col

    def get_row(self, row_index: int) -> list:
        row = []
        for i in range(0, self.__num_cols):
            row.append(self.__matrix[i, row_index])
        return row

    def get_num_rows(self) -> int:
        return self.__num_rows

    def get_num_cols(self) -> int:
        return self.__num_cols
