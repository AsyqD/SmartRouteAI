import streamlit as st
import pandas as pd
import numpy as np  
#import matplotlib.pyplot as plt
#import seaborn as sns
from department_knowledge_base import DEPARTMENT_KNOWLEDGE
import json
from datetime import datetime
import llm_agent
import loghandler

        

# Function to extract JSON from text
def get_json_from_text(text: str) -> dict:
    """
    Преобразует текст в JSON-объект.
    """
    try:
        t_text = text[text.rfind('{'):text.rfind('}')+1].replace('\n  ', '')
        return json.loads(t_text)
    except json.JSONDecodeError as e:
        st.error(f"Ошибка при разборе JSON: {e}")
        return {}
    
if __name__ == "__main__":
    
    
    llm_agent = llm_agent.LMStudioClient()
    
    # Set up Streamlit app
    st.image(
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Halyk_Bank.svg/1200px-Halyk_Bank.svg.png",
    )
    st.title('Halyk Bank')
    st.write('This is a simple Streamlit app to demonstrate basic functionality.')


    name = st.text_input('Enter your name:')
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
            
        start_time = datetime.now()
            
        # Here you would typically call your model to get a response
        full_response = llm_agent.classify_query(add_prompt)
        response = get_json_from_text(full_response)
        end_time = datetime.now()
        
        # Log the classification
        loghandler.log_classification(
            user_name=name,
            department=department,
            prompt=add_prompt,
            response_json=response,
            response_time=(end_time - start_time).total_seconds()
        )

        if not response:
            st.error("Не удалось получить ответ от модели. Проверьте форматирование запроса.")
            st.stop()
            
            
        response_prompt = f"""**Обращение: "{response['urgency']}". Направление в работу для "{response['department']}":**\n\n{response['summary']}\n"""
        
        with st.chat_message("assistant"):
            st.write(response_prompt)