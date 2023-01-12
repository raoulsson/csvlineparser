import logging

from src.csvlineparser.csv_consumer_interface import ICsvConsumer

logger = logging.getLogger(__name__)


class CsvConsoleConsumer(ICsvConsumer):

    def __init__(self) -> None:
        super().__init__()
        self.__colIndex = 0
        self.__rowIndex = 0
        self.__numCols = 0
        self.__numRows = 0
        self.__matrix = {}

    def consumeField(self, s: str) -> None:
        self.__matrix[self.__colIndex, self.__rowIndex] = s
        self.__colIndex += 1
        if self.__numCols < self.__colIndex:
            self.__numCols += 1

    def signalEndOfRecord(self) -> None:
        self.__rowIndex += 1
        self.__numRows += 1
        self.__colIndex = 0

    def signalEndOfFile(self) -> None:
        print(f'End of file reached. Got {self.__numCols} columns and {self.__numRows} rows')

    def getMatrix(self) -> dict:
        return self.__matrix

    def getColumn(self, colIndex: int) -> list:
        col = []
        for i in range(0, self.__numRows):
            col.append(self.__matrix[colIndex, i])
        return col

    def getRow(self, rowIndex: int) -> list:
        row = []
        for i in range(0, self.__numCols):
            row.append(self.__matrix[i, rowIndex])
        return row

    def getNumRows(self) -> int:
        return self.__numRows

    def geNumCols(self) -> int:
        return self.__numCols
