from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class BusinessNews:
    country_code: str
    content: List[Dict[str, str]]
    created_at: datetime
