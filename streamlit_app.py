import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login


# login
sign = Login(st.secrets["email"], st.secrets["pass"])
cookies = sign.login()
#sign.saveCookies()

st.set_page_config(page_title="Streamlit ChatBot")

# Initialize empty lists to store AI generated responses and past user inputs
if 'g_response' not in st.session_state:
    st.session_state['g_response'] = ["Welcome to EnzoChat, How may I help you?"]
if 'p_response' not in st.session_state:
    st.session_state['p_response'] = ['Hi!']

# Defining the layout for input and response containers
inputContainer = st.container()
colored_header(label='', description='', color_name='blue-30')
respContainer = st.container()

# Function to receive user input prompt
def get_text():
    inputText = st.text_input("You: ", "", key="input")
    return inputText
with inputContainer:
    userInput = get_text()

# Function to receive user prompt and generate AI responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    res = chatbot.query(prompt)
    return res

# Display AI generated responses based on user prompts
with respContainer:
    if userInput:
        res = generate_response(userInput)
        st.session_state.p_response.append(userInput)
        st.session_state.g_response.append(res)
        
    if st.session_state['g_response']:
        for i in range(len(st.session_state['g_response'])):
            message(str(st.session_state['p_response'][i]), is_user=True, key=str(i) + '_user')
            message(str(st.session_state["g_response"][i]), key=str(i))
