from typing import List
from decimal import Decimal

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
        color: str,
        estimated_monthly_cost: Decimal,
    ) -> Category:
        if not name.strip():
            raise BusinessException(
                ErrorCode.INVALID_PARAMETER,
                "Category name cannot be empty",
            )

        if estimated_monthly_cost < 0:
            raise BusinessException(
                ErrorCode.INVALID_PARAMETER,
                "Estimated cost cannot be negative",
            )

        category = Category.create(
            user_id=user_id.value,
            name=name,
            color=color,
            estimated_monthly_cost=estimated_monthly_cost,
        )

        self.repository.save(category)
        return category

    def delete_category(self, category_id: CategoryId) -> None:
        existing = self.repository.find_by_id(category_id)

        if existing is None:
            raise BusinessException(
                ErrorCode.DATA_NOT_FOUND,
                f"Category not found: {category_id.value}",
            )

        self.repository.delete(category_id)

    def list_categories(self, user_id: UserId) -> List[Category]:
        return self.repository.find_by_user(user_id)
