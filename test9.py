import streamlit as st
import os
from groq import Groq
import random
import base64

from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

st.set_page_config(
    page_title="OISON",
    
)
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

def autoplay_audio2(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# Load sound files
# sound1 = "sound1.mp3"
# sound2 = "sound2.mp3"

hide_streamlit_style = """
<style>
.css-1y0tads {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# enable_scroll = """
# <style>
# .main {
#     overflow: auto;
# }
# </style>
# """

# st.markdown(enable_scroll, unsafe_allow_html=True)
options = {
        'show_menu': False
        }
    
# Function to play sound1 when user enters a prompt
# def play_sound1():
#     st.audio(sound1, format="audio/mp3", start_time=0, autoplay=True)

# # Function to play sound2 when bot responds
# def play_sound2():
#     st.audio(sound2, format="audio/mp3", start_time=0, autoplay=True)

def main():

    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
   


    
    # Get Groq API key
    groq_api_key = "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"

    # Display the Groq logo
    #spacer, col = st.columns([5, 1])  
    #with col:  
    #    st.image('groqcloud_darkmode.png')

    # The title and greeting message of the Streamlit application
    st.title("Mr.OISON")
    st.markdown("""
 Hello! I'm OISON.
 I can help answer your questions about any of the following topics:
- **Mental Health**
- **Business Health**
- **Investment Health**

I'm also super fast! Let's start our conversation!
""")


    # Add customization options to the sidebar
    # st.sidebar.title('Customization')
    # system_prompt = st.sidebar.text_input("System prompt:")
    model = 'llama3-8b-8192'
    conversational_memory_length = 50

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

  
    user_question = st.chat_input("Ask a question!")


    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context(
                {'input':message['human']},
                {'output':message['AI']}
                )


    

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )


    # If the user has asked a question,
    if user_question:
       
        
        # play_sound1()
        # Construct a chat prompt template using various components
        prompt = ChatPromptTemplate.from_messages(
            
            [
                 # This is the persistent system prompt that is always included at the start of the chat.

                # MessagesPlaceholder(
                #     variable_name="chat_history"
                # ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.
                
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # This template is where the user's current input will be injected into the prompt.
                
            ]
            

        )


        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        conversation = LLMChain(
            llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
            prompt=prompt,  # The constructed prompt template.
            verbose=True,   # Enables verbose output, which can be useful for debugging.
            memory=memory,  # The conversational memory object that stores and manages the conversation history.
        )
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation.predict(human_input=user_question)
        message = {'human':user_question,'AI':response}
        st.session_state.chat_history.append(message)
        # Play sound2 when output is sent back
        # play_sound2()

        # st.write("Chatbot:", response)


         # Displaying chat history vertically with fixed height and vertical scrolling
        
        chat_history_display = "<div style='overflow-y: scroll;'>"
        # Load sound files
        sound1 = "sound1.mp3"
        sound2 = "sound2.mp3"
        for msg in st.session_state.chat_history:
             
            autoplay_audio("sound1.mp3")
            # st.audio(sound1, format="audio/mp3", start_time=0, autoplay=True)  
            chat_history_display += f"<div><b style='margin-left: 10px;'>You:</b></div><div style='background-color: #0073cf; color:white;border-radius: 8px; padding: 5px;margin-right: 20%;'><span style='margin-left: 20px;'>{msg['human']}</span></div>"
            autoplay_audio2("sound2.mp3")
            chat_history_display += f"<div style='text-align: right;'><b style='margin-left: 10px;'>Adam:</b></div><div style='background-color: black; color:white;border-radius: 8px; padding: 5px; margin-left: 10%;;'><span style='margin-right: 20px;'>{msg['AI']}</span></div><br>"
            
            
        chat_history_display += "</div>"
        
        st.markdown(chat_history_display, unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()