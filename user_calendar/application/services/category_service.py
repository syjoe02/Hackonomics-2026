from typing import List

from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException

from user_calendar.domain.entities import Category
from user_calendar.domain.value_objects import CategoryId, UserId
from user_calendar.application.ports.repository import CategoryRepository

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(
        self,
        user_id: UserId,
        name: str,
        color: str | None = None,
    ) -> Category:
        if not name or not name.strip():
            raise BusinessException(ErrorCode.INVALID_PARAMETER)
        # Default color
        color = "#3b82f6"

        category = Category.create(
            user_id=user_id,
            name=name,
            color=color,
        )
        self.repository.save(category)
        return category

    def delete_category(self, category_id: CategoryId, user_id: UserId) -> None:
        existing = self.repository.find_by_id(category_id)

        if existing is None:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)
        if existing.user_id.value != user_id.value:
            raise BusinessException(ErrorCode.FORBIDDEN)
        self.repository.delete(category_id)

    def list_categories(self, user_id: UserId) -> List[Category]:
        return self.repository.find_by_user_id(user_id)
