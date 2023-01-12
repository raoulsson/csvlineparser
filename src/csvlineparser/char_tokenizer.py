import logging
from abc import ABC

from src.csvlineparser.char_tokenizer_interface import ICharTokenizer
from src.csvlineparser.exceptions import CharTokenizerException

logger = logging.getLogger(__name__)


class StringCharTokenizer(ICharTokenizer, ABC):

    def __init__(self, s: str) -> None:
        super().__init__()
        self.__s: str = s
        self.__index: int = 0
        self.__haveUnreadChar: bool = False
        self.__unreadChar: str = ''

    def __skipCrInCrLf(self) -> None:
        if self.__s[self.__index] == '\r' and self.__index + 1 < len(self.__s) and self.__s[self.__index + 1] == '\n':
            self.__index += 1

    def __mapCrToLf(self, c: str) -> str:
        if c == '\r':
            return '\n'
        return c

    def peek(self) -> str:
        if self.__haveUnreadChar:
            return self.__unreadChar
        if self.__index < len(self.__s):
            return self.__mapCrToLf(self.__s[self.__index])
        return 'EOF'

    def read(self) -> str:
        if self.__haveUnreadChar:
            self.__haveUnreadChar = False
            return self.__unreadChar
        if self.__index < len(self.__s):
            self.__skipCrInCrLf()
            ret_val = self.__mapCrToLf(self.__s[self.__index])
            self.__index += 1
            return ret_val
        return 'EOF'

    def unread(self, c: str) -> None:
        if self.__haveUnreadChar:
            raise CharTokenizerException('unread() cannot accept more than one pushed back character')
        self.__haveUnreadChar = True
        self.__unreadChar = c

    def getPos(self) -> int:
        return self.__index

    def getSegment(self, offset: int, length: int) -> str:
        return self.__s[offset:offset + length]
