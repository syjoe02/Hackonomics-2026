from abc import ABC, abstractmethod
from typing import Dict

class EventConsumerPort(ABC):

    @abstractmethod
    def consume(self, event: Dict):
        pass