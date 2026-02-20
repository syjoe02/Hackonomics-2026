from typing import Any, Dict, List


def validate_news_items(data: Any) -> List[Dict]:
    if not isinstance(data, list):
        return []

    valid = []
    for item in data:
        if not isinstance(item, dict):
            continue

        title = item.get("title")
        desc = item.get("description")

        if title and desc:
            valid.append(
                {
                    "title": str(title),
                    "description": str(desc),
                }
            )

    return valid[:5]
