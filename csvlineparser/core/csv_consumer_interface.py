import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ICsvConsumer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def consume_field(self, s: str) -> None:
        pass

    @abstractmethod
    def signal_end_of_record(self) -> None:
        pass

    @abstractmethod
    def signal_end_of_line(self) -> None:
        pass
