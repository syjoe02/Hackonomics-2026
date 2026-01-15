# Django Archiecture

```
Domain / UseCase <- ports/api (interface) <- adapter (ORM, external API)
```

# 1차

(A) 마이페이지: 국가/기준통화 + 기본 프로필
	•	국가 선택 (KRW 기준 가정 OK)
	•	월 소득or연 소득, 저축 기간(예: 1년/2년), 위험 선호(보수/중립/공격)

(B) 매일 09:00 환율 스냅샷 + 변동률
	•	USD/KRW, EUR/KRW
	•	전일 대비 % 변화, 7일 변화
	•	“왜 중요한지” 한 줄 설명(LLM)

(C) 캘린더에 월 소득과 지출