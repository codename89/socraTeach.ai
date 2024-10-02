import streamlit as st
import google.generativeai as genai

class SocraticTeachingAssistant:
    def __init__(self):
        self.knowledge_base = self.init_knowledge_base()
        self.current_topic = None
        self.chat_session = None
        self.model = None
        self.difficulty = "medium"  # Default difficulty
        self.mode = "Socratic"  # Default mode

    def configure_gemini(self, api_key):
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

    def init_knowledge_base(self):
        return {
            "sorting": ["bubble sort", "quick sort", "merge sort"],
            "searching": ["linear search", "binary search"],
            "data structures": ["array", "linked list", "tree", "graph"],
        }

    def start_conversation(self, topic, api_key, difficulty):
        self.configure_gemini(api_key)
        if topic not in self.knowledge_base:
            return f"I'm sorry, I don't have information about {topic}. Let's discuss sorting, searching, or data structures."

        self.current_topic = topic
        self.difficulty = difficulty
        self.chat_session = self.model.start_chat(history=[])

        system_prompt = f"""
        You are a teaching assistant specializing in Data Structures and Algorithms, 
        particularly in {topic}. Your goal is to help the student understand {topic}.
        Focus on concepts like: {', '.join(self.knowledge_base[topic])}.
        The current difficulty level is set to {difficulty}. Adjust your explanations accordingly.
        For 'easy', use simpler terms and basic concepts. For 'medium', introduce more detailed explanations. 
        For 'hard', delve into complex details and edge cases.
        """

        self.chat_session.send_system_message(system_prompt)

        return "Conversation started! Let's dive into the topic."

    def process_response(self, message):
        if not self.chat_session:
            return "Please start a conversation first by choosing a topic."

        response = self.chat_session.send_user_message(message)

        if self.mode == "Socratic":
            return f"Asking a guiding question: {response}"
        elif self.mode == "Q&A":
            return f"Answering the question: {response}"

    def switch_mode(self, new_mode):
        self.mode = new_mode
        return f"Switched to {new_mode} mode."

    def end_conversation(self):
        self.chat_session = None
        self.current_topic = None
        return "Conversation ended."


# Initialize Streamlit app
st.title("Socratic Teaching Assistant")
assistant = SocraticTeachingAssistant()

# Initialize session state variables if not already
if 'conversation_active' not in st.session_state:
    st.session_state.conversation_active = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'mode' not in st.session_state:
    st.session_state.mode = "Socratic"

# Sidebar: Select topic, difficulty, and API key
st.sidebar.subheader("Conversation Settings")
api_key = st.sidebar.text_input("Enter API key", type="password")
topic = st.sidebar.selectbox("Select a topic", options=["sorting", "searching", "data structures"])
difficulty = st.sidebar.selectbox("Select difficulty", options=["easy", "medium", "hard"])

# Button to start conversation
if st.sidebar.button("Start Conversation") and api_key:
    response = assistant.start_conversation(topic, api_key, difficulty)
    st.session_state.conversation_active = True
    st.session_state.messages.append(("assistant", response))
    st.session_state.mode = "Socratic"

# Mode selection and explanation (outside the sidebar)
if st.session_state.get("conversation_active"):
    st.subheader("Interaction Mode")
    col1, col2 = st.columns(2)
    with col1:
        new_mode = st.radio("Select mode:", ["Socratic", "Q&A"])
        if new_mode != st.session_state.get("mode"):
            response = assistant.switch_mode(new_mode)
            st.session_state.messages.append(("assistant", response))
            st.session_state.mode = new_mode
            st.rerun()
    with col2:
        if st.session_state.get("mode") == "Socratic":
            st.info("In Socratic mode, the assistant will guide you through learning using questions and prompts.")
        else:
            st.info("In Q&A mode, you can ask direct questions about the current topic, and the assistant will provide answers.")

# Display conversation history
if st.session_state.get("messages"):
    for role, message in st.session_state.get("messages"):
        with st.chat_message(role):
            st.write(message)

# User input
if st.session_state.get("conversation_active") and api_key:
    user_input = st.chat_input("Your response:" if st.session_state.get("mode") == "Socratic" else "Your question:")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        assistant_response = assistant.process_response(user_input)
        st.session_state.messages.append(("assistant", assistant_response))
        st.rerun()

# Option to start a new conversation
if st.session_state.get("conversation_active"):
    if st.button("Start New Conversation"):
        st.session_state.conversation_active = False
        st.session_state.messages = []
        st.rerun()
