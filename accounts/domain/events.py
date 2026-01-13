from dataclasses import dataclass

@dataclass(frozen=True)
class AccountUpdated:
    user_id : int