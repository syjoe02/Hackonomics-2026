from abc import ABC, abstractmethod


class BusinessNewsPort(ABC):

    @abstractmethod
    def get_country_news(self, country_code: str) -> str:
        pass
