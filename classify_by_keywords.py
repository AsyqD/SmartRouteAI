# Реализация простого классификатора запросов по ключевым словам уогда не работает LLM модель
from typing import Tuple

from department_knowledge_base import DEPARTMENT_KNOWLEDGE

def classify_by_keywords(query_text: str):
    """
    Простой классификатор на основе ключевых слов.
    Возвращает:
        - Название департамента
        - Оценка срочности ("Срочно", "Репутационно", "Обычное")
        - Краткое описание запроса
    """
    query_lower = query_text.lower()

    for dep in DEPARTMENT_KNOWLEDGE:
        for keyword in dep["keywords"]:
            if keyword.lower() in query_lower:
                urgency = "Срочно" if any(k in query_lower for k in ["полиция", "жалоба", "угроза", "репутация"]) else "Обычное"
                return dep["name"], urgency, f"Запрос: {query_text[:50]}..." if len(query_text) > 50 else query_text

    # fallback
    return "Служба поддержки / Call-центр", "Обычное", f"Запрос: {query_text[:50]}..." if len(query_text) > 50 else query_text
