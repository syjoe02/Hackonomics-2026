from dataclasses import dataclass
from datetime import datetime


@dataclass
class BusinessNews:
    country_code: str
    content: str
    created_at: datetime
