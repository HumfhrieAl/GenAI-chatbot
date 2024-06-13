from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    # Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
    st.subheader("The chat history is")
    
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")