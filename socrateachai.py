import streamlit as st
import google.generativeai as genai
from PIL import Image

class SocraticTeachingAssistant:
    def __init__(self):
        self.knowledge_base = {
            "sorting": ["bubble sort", "quick sort", "merge sort"],
            "searching": ["linear search", "binary search"],
            "data structures": ["array", "linked list", "tree", "graph"],
        }
        self.current_topic = None
        self.chat_session = None
        self.model = None
        self.difficulty = "medium"
        self.mode = "Socratic"

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

    def start_conversation(self, topic, difficulty):
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
        For 'easy', use simpler terms and basic concepts. For 'medium', introduce more complex ideas.
        For 'hard', challenge the student with advanced concepts and edge cases.
        The current mode is {self.mode}. In Socratic mode, guide through questions. In Q&A mode, provide direct answers.
        Start by asking what the student already knows about {topic}, keeping in mind the {difficulty} difficulty level.
        """

        response = self.chat_session.send_message(system_prompt)
        return response.text

    def process_response(self, user_input):
        if not self.chat_session:
            return "Please start a conversation first by choosing a topic."

        if self.mode == "Socratic":
            prompt = f"""
            The student's response was: "{user_input}"
            Analyze their understanding and formulate a Socratic question to deepen their knowledge 
            of {self.current_topic}. Remember to guide them towards understanding rather than 
            providing direct answers. If they seem confused, break down the concept further.
            If they show understanding, challenge them with a more advanced aspect of {self.current_topic}.
            Keep in mind that the current difficulty level is {self.difficulty}.
            For 'easy', use simpler terms and focus on basic concepts.
            For 'medium', introduce more complex ideas and terminology.
            For 'hard', challenge the student with advanced concepts, edge cases, and deeper analysis.
            """
        else:  # Q&A mode
            prompt = f"""
            The student's question was: "{user_input}"
            Provide a clear, concise, and direct answer about {self.current_topic}. 
            If the question asks for code, include a relevant code snippet.
            Do not use the Socratic method or ask the student to think about the process themselves.
            If the question is not directly related to {self.current_topic}, provide a brief answer 
            and gently redirect to the current topic.
            Keep in mind that the current difficulty level is {self.difficulty}.
            """

        response = self.chat_session.send_message(prompt)
        return response.text

    def change_difficulty(self, new_difficulty):
        if new_difficulty not in ["easy", "medium", "hard"]:
            return "Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'."

        self.difficulty = new_difficulty
        prompt = f"""
        The difficulty level has been changed to {new_difficulty}. Adjust your teaching approach accordingly.
        For 'easy', use simpler terms and focus on basic concepts.
        For 'medium', introduce more complex ideas and terminology.
        For 'hard', challenge the student with advanced concepts, edge cases, and deeper analysis.
        Inform the student about the change and ask an appropriate question to continue the lesson at the new difficulty level.
        """

        response = self.chat_session.send_message(prompt)
        return response.text

    def switch_mode(self, new_mode):
        self.mode = new_mode
        prompt = f"""
        The conversation mode has been switched to {new_mode} mode.
        For Socratic mode, use questions to guide the student's learning about {self.current_topic}.
        For Q&A mode, provide direct and concise answers about {self.current_topic}.
        Respond with an appropriate message to acknowledge the mode change and set the tone for the new mode.
        """
        response = self.chat_session.send_message(prompt)
        return response.text

    def check_understanding(self):
        prompt = f"""
        Based on the conversation so far about {self.current_topic}, provide the following:
        1. A brief summary (2-3 sentences) of what we've discussed and the main concepts covered.
        2. An assessment of the student's current understanding, noting any areas of strength or confusion.
        3. A question or set of options for the student to choose from, such as:
        a) Would you like to dive deeper into any specific aspect of {self.current_topic}?
        b) Are you ready to move on to a related topic? If so, I can suggest some options.
        c) Do you feel you've grasped the main concepts and want to conclude this topic?
        d) Are there any parts of {self.current_topic} you'd like me to explain differently?
        
        Present this information clearly and concisely, maintaining a supportive and encouraging tone.
        """
        response = self.chat_session.send_message(prompt)
        return response.text

    def conclude_topic(self):
        prompt = f"""
        Provide a concise summary of the key points discussed about {self.current_topic}.
        Highlight the main concepts learned, any problem-solving strategies introduced, and suggestions for further study.
        End with an encouraging message about applying this knowledge to real-world programming challenges.
        """
        response = self.chat_session.send_message(prompt)
        return response.text

    def end_conversation(self):
        if not self.chat_session:
            return "No active conversation to end."

        self.current_topic = None
        self.chat_session = None
        self.model = None
        self.difficulty = "medium"
        self.mode = "Socratic"
        return "Thank you for the discussion. Is there anything else you'd like to explore?"

# Initialize the teaching assistant
assistant = SocraticTeachingAssistant()

# Streamlit UI
st.set_page_config(page_title="Socratic Teaching Assistant", layout="wide")

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

# Function to start a new conversation
def start_new_conversation():
    st.session_state.messages = []
    st.session_state.conversation_active = False
    assistant.difficulty = "medium"
    assistant.mode = "Socratic"

# Sidebar for topic selection, difficulty, and conversation control
with st.sidebar:
    if not api_key:
        st.error("Please enter your Gemini API Key to start.")
    elif not st.session_state.conversation_active:
        st.subheader("Start a New Conversation")
        topics = list(assistant.knowledge_base.keys())
        selected_topic = st.selectbox("Choose a topic:", topics)
        difficulty = st.select_slider("Select difficulty:", options=["easy", "medium", "hard"], value="medium")
        if st.button("Start Conversation"):
            assistant.configure_gemini(api_key)
            response = assistant.start_conversation(selected_topic, difficulty)
            st.session_state.messages.append(("assistant", response))
            st.session_state.conversation_active = True
            st.rerun()
    else:
        st.subheader("Conversation Settings")
        new_difficulty = st.select_slider("Adjust difficulty:", options=["easy", "medium", "hard"], value=assistant.difficulty)
        if new_difficulty != assistant.difficulty:
            response = assistant.change_difficulty(new_difficulty)
            st.session_state.messages.append(("assistant", response))
            st.rerun()
        
        if st.button("Check Understanding"):
            response = assistant.check_understanding()
            st.session_state.messages.append(("assistant", response))
            st.rerun()

        if st.button("Conclude Topic"):
            response = assistant.conclude_topic()
            st.session_state.messages.append(("assistant", response))
            st.session_state.conversation_active = False
            st.rerun()

        if st.button("End Conversation"):
            response = assistant.end_conversation()
            st.session_state.messages.append(("assistant", response))
            st.session_state.conversation_active = False
            st.rerun()

# Mode selection and explanation (outside the sidebar)
if st.session_state.conversation_active:
    st.subheader("Interaction Mode")
    col1, col2 = st.columns(2)
    with col1:
        new_mode = st.radio("Select mode:", ["Socratic", "Q&A"])
        if new_mode != assistant.mode:
            response = assistant.switch_mode(new_mode)
            st.session_state.messages.append(("assistant", response))
            st.rerun()
    with col2:
        if assistant.mode == "Socratic":
            st.info("In Socratic mode, the assistant will guide you through learning using questions and prompts.")
        else:
            st.info("In Q&A mode, you can ask direct questions about the current topic, and the assistant will provide answers.")

# Display conversation history
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)

# User input
if st.session_state.conversation_active and api_key:
    user_input = st.chat_input("Your response:" if assistant.mode == "Socratic" else "Your question:")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        response = assistant.process_response(user_input)
        st.session_state.messages.append(("assistant", response))
        st.rerun()

# Option to start a new conversation
if st.session_state.conversation_active:
    if st.button("Start New Conversation"):
        start_new_conversation()
        st.rerun()