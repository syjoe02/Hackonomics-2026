from typing import Optional, Protocol

from accounts.domain.entities import Account


class AccountRepository(Protocol):
    def find_by_user_id(self, user_id: int) -> Optional[Account]: ...

    def save(self, account: Account) -> None: ...
