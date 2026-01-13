from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in



@receiver(user_logged_in)
def ensure_account_on_login(sender, request, user, **kwargs):
    from accounts.application.usecases import UpdateAccountUseCase
    from accounts.application.dto import AccountUpdateCommand
    from accounts.adapters.orm.repository import DjangoAccountRepository
    from accounts.adapters.events.publisher import OutboxEventAdapter
    
    repo = DjangoAccountRepository()
    existing = repo.find_by_user_id(user.id)
    if existing:
        return
    
    usecase = UpdateAccountUseCase(
        repository=repo,
        event_publisher=OutboxEventAdapter(),
    )

    command = AccountUpdateCommand(
        country_code="KR",
        currency="KRW",
        annual_income=30_000_000,
        monthly_investable_amount=500_000
    )

    usecase.execute(
        user_id=user.id,
        command=command,
    )