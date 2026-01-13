from typing import Protocol, Dict, Any

class DomainEventPublisher(Protocol):
    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        ...
