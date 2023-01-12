import logging
from abc import ABC

from csvlineparser.char_tokenizer_interface import ICharTokenizer
from csvlineparser.exceptions import CharTokenizerException

logger = logging.getLogger(__name__)


class StringCharTokenizer(ICharTokenizer, ABC):

    def __init__(self, s: str) -> None:
        super().__init__()
        self.__s: str = s
        self.__index: int = 0
        self.__have_unread_char: bool = False
        self.__unread_char: str = ''

    def __skipCrInCrLf(self) -> None:
        if self.__s[self.__index] == '\r' and self.__index + 1 < len(self.__s) and self.__s[self.__index + 1] == '\n':
            self.__index += 1

    def __mapCrToLf(self, c: str) -> str:
        if c == '\r':
            return '\n'
        return c

    def peek(self) -> str:
        if self.__have_unread_char:
            return self.__unread_char
        if self.__index < len(self.__s):
            return self.__mapCrToLf(self.__s[self.__index])
        return 'EOF'

    def read(self) -> str:
        if self.__have_unread_char:
            self.__have_unread_char = False
            return self.__unread_char
        if self.__index < len(self.__s):
            self.__skipCrInCrLf()
            ret_val = self.__mapCrToLf(self.__s[self.__index])
            self.__index += 1
            return ret_val
        return 'EOF'

    def unread(self, c: str) -> None:
        if self.__have_unread_char:
            raise CharTokenizerException('unread() cannot accept more than one pushed back character')
        self.__have_unread_char = True
        self.__unread_char = c

    def get_pos(self) -> int:
        return self.__index

    def get_segment(self, offset: int, length: int) -> str:
        return self.__s[offset:offset + length]
