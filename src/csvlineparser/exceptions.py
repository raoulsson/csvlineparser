import logging

logger = logging.getLogger(__name__)


class CharTokenizerException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class CsvParserTooMuchDataException(Exception):

    def __init__(self, message: str, pos: int, data: str, offset: int, lineNumber: int):
        super().__init__(self, message)
        data = data.replace('\r', '\\r').replace('\n', '\\n')
        print(f'line: {lineNumber}, pos: {pos}')
        print(f'{data}')
        print(f'{"-" * offset}^')


class CsvParserNoTermQuoteException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class IllegalArgumentException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)