import streamlit as st 


st.set_page_config(
    page_title="BlackSheep-ThinkingFlow-Math-Demo",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "KEY" not in st.session_state:
    st.session_state["KEY"] = ""
    
    
with st.sidebar:
    st.title('🤖️📖 MATH PROLBEM SOLVER')

    st.subheader('METHOD: ')
    selected_type = st.sidebar.selectbox('Choose a thinking-flow', ['retrieval', 'non-retrieval'], key='selected_type')

        
if st.session_state["KEY"] == "":
    st.session_state["KEY"] = st.secrets["KEY"]
else:
    import os  
    import openai 
    openai.api_key = st.session_state["KEY"]
    os.environ["OPENAI_API_KEY"] = st.session_state["KEY"] 
    
if st.session_state["KEY"] == "":
    st.stop() 
    
import sys  
sys.path.append("..")
from src.SolvingMachine import SolvingMachine

# TODO: complete this part for non-coding using
    





