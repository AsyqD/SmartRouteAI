from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from datetime import datetime
import logging

class LMStudioClient:
    def __init__(self, base_url="http://127.0.0.1:1234/v1", api_key="sk-local"):
        self.base_url = base_url
        self.api_key = api_key
        self.llm = ChatOpenAI(
            model="DeepSeekR1-8b-Qwen3-8b",
            base_url=base_url, 
            api_key=api_key, 
        )
        
    def classify_query(self, text: str) -> str:
        from department_knowledge_base import DEPARTMENT_KNOWLEDGE
        depsartment_names = "\n".join([f"{d['name']}: {d['description']}" for d in DEPARTMENT_KNOWLEDGE])
        
        messages =  [SystemMessage(content=f'''
Ты — помощник банка, который классифицирует обращения к Банку. 

Твоя задача — следовать этим инструкциям:
1. Анализируй предоставленное обращение 
2. Определяешь подразделение банка (department)
3. Оцениваешь срочность (urgency)
4. Формулируешь краткое содержание (summary)
5. Возвращаешь ТОЛЬКО валидный JSON-объект без каких-либо пояснений

Доступные категории:
- Подразделения (department): {depsartment_names}
- Срочность (urgency): "Срочно" (финансовые потери/блокировка), "Репутационно" (риск для имиджа), "Обычное" (стандартные вопросы)

Правила summary:
- Только факты из обращения
- Без эмоциональной оценки
Верни ТОЛЬКО JSON в таком формате (без комментариев до/после):
{{
  "department": "выбранное_подразделение",
  "urgency": "уровень_срочности",
  "summary": "опиши обращение для работы департаменту и желаемые результаты и действия от банка"

}}'''),
        HumanMessage(content=text)
    ]
    

  
        response = self.llm.invoke(messages)
        return response.content
    
