from common.errors.error_codes import ErrorCode
from common.errors.exceptions import BusinessException


class LlmNewsService:
    def __init__(self, account_repo, news_repo, rag_hybrid, rag_rerank):
        self.account_repo = account_repo
        self.news_repo = news_repo
        self.rag_hybrid = rag_hybrid
        self.rag_rerank = rag_rerank

    def prepare_llm_payload(self, user_id: str, question: str):
        if not question or not question.strip():
            raise BusinessException(ErrorCode.MISSING_REQUIRED_FIELD)

        account = self.account_repo.find_by_user_id(int(user_id))
        if not account:
            raise BusinessException(ErrorCode.USER_NOT_FOUND)

        country_code = account.country.code

        candidates = self.rag_hybrid.search(
            question=question,
            country_code=country_code,
            top_k=10,
        )

        if not candidates:
            latest = self.news_repo.get_latest_news(country_code)
            if not latest:
                raise BusinessException(ErrorCode.DATA_NOT_FOUND)
            candidates = latest[:10]

        contexts = self.rag_rerank.rerank_news(
            question=question,
            candidates=candidates,
            top_k=3,
        )

        if not contexts:
            raise BusinessException(ErrorCode.DATA_NOT_FOUND)

        return {
            "user_id": str(user_id),
            "question": question,
            "news": contexts,
        }
