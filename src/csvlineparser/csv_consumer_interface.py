import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ICsvConsumer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def consumeField(self, s: str) -> None:
        pass

    @abstractmethod
    def signalEndOfRecord(self) -> None:
        pass

    @abstractmethod
    def signalEndOfFile(self) -> None:
        pass
