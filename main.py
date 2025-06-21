import streamlit as st
import pandas as pd
import numpy as np  
#import matplotlib.pyplot as plt
#import seaborn as sns
from department_knowledge_base import DEPARTMENT_KNOWLEDGE
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.messages import AIMessage
import json

llm = OpenAI(
    model="local-model",
    temperature=0,
    base_url="http://127.0.0.1:1234",
    api_key="sk-local",  # replace with your actual OpenAI API key
    organization="org-local",  # replace with your actual OpenAI organization ID
    ) # replace with your actual OpenAI API key and organization ID
    #api_base="https://api.openai.com/v1",  # Optional, if you need to specify a different base URL 

def classify_query_with_local_llm(text):
    messages = [
        SystemMessage(content="Ты помощник банка. Классифицируй обращение."),
        HumanMessage(content=f"""
        Обращение: "{text}"

        Ответь в формате JSON:
        {{
          "department": "...",
          "urgency": "Срочно/Репутационно/Обычное",
          "summary": "краткое описание запроса"
        }}
        """)
    ]
    try:
        response = llm(messages).content
        result = json.loads(response)
        return result["department"], result["urgency"], result["summary"]
    except Exception as e:
        return "Служба поддержки / Call-центр", "Обычное", f"Запрос: {text[:50]}..."

st.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Halyk_Bank.svg/1200px-Halyk_Bank.svg.png",
    #width=200,  # adjust size as needed
    #height=100,  # adjust size as needed
    #use_column_width=True,
    
    #caption="Halyk Bank"
)
st.title('Halyk Bank')
st.write('Hello, World!')
name = st.text_input('Enter your name:', 'John Doe')
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
    add_prompt = f"{name} из {department}: {prompt}"
    st.session_state.messages.append({"role": "user", "content": f"{name} из {department}: {prompt}"})
    with st.chat_message("user"):
        st.write(add_prompt)

    # Here you would typically call your model to get a response
    response = f"You said: {prompt}"  # Placeholder response
    #department_llm, urgency_llm, summary_llm = classify_query_with_local_llm(add_prompt)

    #response = f"Классификация: Департамент: {department_llm}, Срочность: {urgency_llm}, Описание: {summary_llm}"
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)