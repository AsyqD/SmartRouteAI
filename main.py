import streamlit as st
import pandas as pd
import numpy as np  
#import matplotlib.pyplot as plt
#import seaborn as sns
from department_knowledge_base import DEPARTMENT_KNOWLEDGE
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

llm = ChatOpenAI(
    model="DeepSeekR1-8b-Qwen3-8b",
    # temperature=0,
    base_url="http://127.0.0.1:1234/v1",  # LM Studio server
    api_key="sk-local",  # replace with your actual OpenAI API key
    # organization="org-local",  # replace with your actual OpenAI organization ID
    )

def classify_query_with_local_llm(text: str) -> str:
    messages =  [SystemMessage(content='''
Ты — помощник банка, который классифицирует обращения к Банку. 

Твоя задача — строго следовать этим инструкциям:
1. Анализируй предоставленное обращение 
2. Определяешь подразделение банка (department)
3. Оцениваешь срочность (urgency)
4. Формулируешь краткое содержание (summary)
5. Возвращаешь ТОЛЬКО валидный JSON-объект без каких-либо пояснений

Доступные категории:
- Подразделения (department): 
- Срочность (urgency): "Срочно" (финансовые потери/блокировка), "Репутационно" (риск для имиджа), "Обычное" (стандартные вопросы)

Правила summary:
- Только факты из обращения
- Без эмоциональной оценки
Верни ТОЛЬКО JSON в таком формате (без комментариев до/после):
{{
  "department": "выбранное_подразделение",
  "urgency": "уровень_срочности",
  "summary": "опиши обращение для работы департаменту и желаемые результаты и действия от банка"

}}'''
    ),
    HumanMessage(content=text)
]
    

  
    response = llm.invoke(messages)
    with open('response.txt', 'w', encoding='utf-8') as f:
        f.write(response.content)
    return response.content
        
    
def get_json_from_text(text: str) -> dict:
    """
    Преобразует текст в JSON-объект.
    """
    try:
        t_text = text[text.rfind('</think>'):]
        return json.loads(t_text)
    except json.JSONDecodeError as e:
        st.error(f"Ошибка при разборе JSON: {e}")
        return {}
# Set up Streamlit app

st.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Halyk_Bank.svg/1200px-Halyk_Bank.svg.png",
    #width=200,  # adjust size as needed
    #height=100,  # adjust size as needed
    #use_column_width=True,
    
    #caption="Halyk Bank"
)
st.title('Halyk Bank')
st.write('Hello, World!')
name = st.text_input('Enter your name:', 'Xavier')
st.write(f'Hello, {name}!')
st.write('This is a simple Streamlit app to demonstrate basic functionality.')
department = st.selectbox(
    'Select a department:',
    [dep['name'] for dep in DEPARTMENT_KNOWLEDGE]
)
if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

with st.chat_message("assistant"):
    st.write("This is a chat message from the assistant.")

if prompt := st.chat_input("Type a message"):
    add_prompt = f"**{name} из {department}:**\n\n{prompt}\n"
    
    st.session_state.messages.append({"role": "user", "content": add_prompt})
    with st.chat_message("user"):
        st.markdown(add_prompt)
    # Here you would typically call your model to get a response
    response =  classify_query_with_local_llm(add_prompt) # Placeholder response
    print(get_json_from_text(response))

    # response = get_json_from_text(response)
    if not response:
        st.error("Не удалось получить ответ от модели. Проверьте форматирование запроса.")
        st.stop()
    # response_prompt = f"""**Обращение: "{response['urgency']}". Направление в работу для "{response['department']}":**\n\n{response['summary']}\n"""
    
    
    # department_llm, urgency_llm, summary_llm = classify_query_with_local_llm(add_prompt)
    # with open('jjj.txt', 'w', encoding='utf-8') as f:
    #     f.write(response)
    # response = f"Классификация: Департамент: {department_llm}, Срочность: {urgency_llm}, Описание: {summary_llm}"
    # st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)