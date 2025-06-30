import streamlit as st
from openai_agent import OpenAIAgent
from deepseek_agent import DeepSeekAgent

st.set_page_config(layout="wide")

container1, container2 = st.columns([0.3, 0.7])

with container1:
    st.markdown("<h1 style='text-align: center;'>Pesquisa</h1>", unsafe_allow_html=True)
    request = st.text_input("Pesquise por um assunto")
    button = st.button("Pesquisar")
    
with container2:
    st.markdown("<h1 style='text-align: center;'>Modelos</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown("<h1 style='text-align: center;'>GPT</h1>", unsafe_allow_html=True)

        if button and request:
            openai_agent = OpenAIAgent()
            opinion = openai_agent.get_opinion(request)
            st.markdown(opinion['opinion'])

    with col2: 
        st.markdown("<h1 style='text-align: center;'>DeepSeek</h1>", unsafe_allow_html=True)

        if button and request:
            deepseek_agent = DeepSeekAgent()
            opinion = deepseek_agent.get_opinion(request)
            st.markdown(opinion['opinion'])
