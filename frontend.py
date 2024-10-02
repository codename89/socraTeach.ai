import streamlit as st
import requests
from PIL import Image

BASE_URL = "http://localhost:8000"

# Load and display the logo
logo = Image.open("logo.png")
st.image(logo, width=200)

st.title("Socratic Teaching Assistant")

# API Key input in sidebar
with st.sidebar:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.warning("Please ensure you keep your API key secure and do not share it.")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'conversation_active' not in st.session_state:
    st.session_state.conversation_active = False

if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "medium"

if 'mode' not in st.session_state:
    st.session_state.mode = "Socratic"

# Function to start a new conversation
def start_new_conversation():
    st.session_state.messages = []
    st.session_state.conversation_active = False
    st.session_state.difficulty = "medium"
    st.session_state.mode = "Socratic"

# Sidebar for topic selection, difficulty, and conversation control
with st.sidebar:
    if not api_key:
        st.error("Please enter your Gemini API Key to start.")
    elif not st.session_state.conversation_active:
        st.subheader("Start a New Conversation")
        response = requests.get(f"{BASE_URL}/available_topics")
        topics = response.json()
        selected_topic = st.selectbox("Choose a topic:", topics)
        difficulty = st.select_slider("Select difficulty:", options=["easy", "medium", "hard"], value="medium")
        if st.button("Start Conversation"):
            response = requests.post(f"{BASE_URL}/start_conversation", json={"topic": selected_topic, "api_key": api_key, "difficulty": difficulty})
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.session_state.conversation_active = True
                st.session_state.difficulty = difficulty
            else:
                st.error("Failed to start conversation. Please check your API key.")
    else:
        st.subheader("Conversation Settings")
        new_difficulty = st.select_slider("Adjust difficulty:", options=["easy", "medium", "hard"], value=st.session_state.difficulty)
        if new_difficulty != st.session_state.difficulty:
            response = requests.post(f"{BASE_URL}/change_difficulty", json={"difficulty": new_difficulty, "api_key": api_key})
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.session_state.difficulty = new_difficulty
                st.rerun()
        
        if st.button("Check Understanding"):
            response = requests.post(f"{BASE_URL}/check_understanding", json={"api_key": api_key})
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.rerun()
            else:
                st.error(f"Failed to check understanding. Status code: {response.status_code}")

        if st.button("Conclude Topic"):
            response = requests.post(f"{BASE_URL}/conclude_topic", json={"api_key": api_key})
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.session_state.conversation_active = False
                st.rerun()
            else:
                st.error(f"Failed to conclude topic. Status code: {response.status_code}")

        if st.button("End Conversation"):
            response = requests.post(f"{BASE_URL}/end_conversation")
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.session_state.conversation_active = False
                st.rerun()
            else:
                st.error(f"Failed to end conversation. Status code: {response.status_code}")

# Mode selection and explanation (outside the sidebar)
if st.session_state.conversation_active:
    st.subheader("Interaction Mode")
    col1, col2 = st.columns(2)
    with col1:
        new_mode = st.radio("Select mode:", ["Socratic", "Q&A"])
        if new_mode != st.session_state.mode:
            response = requests.post(f"{BASE_URL}/switch_mode", json={"message": new_mode, "api_key": api_key})
            if response.status_code == 200:
                st.session_state.messages.append(("assistant", response.json()["response"]))
                st.session_state.mode = new_mode
                st.rerun()
    with col2:
        if st.session_state.mode == "Socratic":
            st.info("In Socratic mode, the assistant will guide you through learning using questions and prompts.")
        else:
            st.info("In Q&A mode, you can ask direct questions about the current topic, and the assistant will provide answers.")

# Display conversation history
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

# User input
if st.session_state.conversation_active and api_key:
    user_input = st.chat_input("Your response:" if st.session_state.mode == "Socratic" else "Your question:")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        response = requests.post(f"{BASE_URL}/process_response", json={"message": user_input, "api_key": api_key})
        
        if response.status_code == 200:
            assistant_response = response.json()["response"]
            st.session_state.messages.append(("assistant", assistant_response))
            st.rerun()
        else:
            st.error("Failed to process response. Please check your API key.")

# Option to start a new conversation
if st.session_state.conversation_active:
    if st.button("Start New Conversation"):
        start_new_conversation()
        st.rerun()