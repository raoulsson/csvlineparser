import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ICharTokenizer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def peek(self) -> str:
        pass

    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def unread(self, char: str) -> str:
        pass

    @abstractmethod
    def getPos(self) -> int:
        pass

    @abstractmethod
    def getSegment(self, offset: int, length: int) -> str:
        pass
