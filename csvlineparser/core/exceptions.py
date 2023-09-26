import logging

logger = logging.getLogger(__name__)


class CharTokenizerException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class CsvParserTooMuchDataException(Exception):

    def __init__(self, message: str, pos: int, data: str, offset: int, line_number: int):
        super().__init__(self, message)
        data = data.replace('\r', '\\r').replace('\n', '\\n')
        logger.info(f'line: {line_number}, pos: {pos}')
        logger.info(f'{data}')
        logger.info(f'{"-" * offset}^')


class CsvParserNoTermQuoteException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class IllegalStateException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class IllegalArgumentException(Exception):

    def __init__(self, message: str):
        super().__init__(self, message)


class IllegalHeaderDataException(Exception):
    """Exception raised for errors in the in file header row.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, __sha256: str):
        self.message = f'Illegal header footprint: {__sha256}'
        super().__init__(self.message)
