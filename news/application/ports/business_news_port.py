from abc import ABC, abstractmethod
from typing import Dict, List


class BusinessNewsPort(ABC):

    @abstractmethod
    def get_country_news(self, country_code: str) -> List[Dict[str, str]]: ...
