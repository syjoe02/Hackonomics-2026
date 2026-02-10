from abc import ABC, abstractmethod


class CalendarAdvisorPort(ABC):
    @abstractmethod
    def analyze_events(self, events_text: str, document_text: str) -> str:
        # Should return AI-generated suggestions in JSON string format.
        pass
