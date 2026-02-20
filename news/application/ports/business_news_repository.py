from abc import ABC, abstractmethod
from typing import Optional

from news.domain.entities import BusinessNews


class BusinessNewsRepository(ABC):

    @abstractmethod
    def find_recent_by_country(self, country_code: str) -> Optional[BusinessNews]:
        pass

    @abstractmethod
    def save(self, news: BusinessNews) -> None:
        pass
