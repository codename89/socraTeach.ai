# socraTeach.ai
![logo](https://github.com/user-attachments/assets/7d81e0b4-2df6-4806-81c4-a03290bc8aa6)

Socratic Teaching Assistant for Data Structures and Algorithms
An interactive AI-powered teaching assistant that uses the Socratic method and direct Q&A to help students learn Data Structures and Algorithms. Built with FastAPI, Streamlit, and Google's Generative AI.
Key Features:

Socratic teaching mode for guided learning
Q&A mode for direct answers
Adjustable difficulty levels
Topics include sorting, searching, and data structures
Interactive web interface
Powered by Google's Gemini AI model

This project aims to provide a scalable, personalized learning experience for computer science students, combining the benefits of Socratic questioning with the convenience of an AI tutor.


## Setup and Running Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- A Google AI Studio account with the Gemini API key
### Setup

1. Clone the repository:
   
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install fastapi uvicorn streamlit google-generativeai pillow
   ```

4. Set up your Google Cloud credentials:
   - Go to the Google AI Studio and sign in to gemini
   - Click get API KEY
   - Create a new project or select an existing one
   - Enable the Gemini API for your project
   - Create an API key and note it down

### Running the Application

1. Start the backend server:
   ```
   python backend.py
   ```
   The backend will be available at `http://localhost:8000`.

2. In a new terminal, start the Streamlit frontend:
   ```
   streamlit run frontend.py
   ```
   The frontend will open in your default web browser with http://localhost:8501.

3. When prompted in the Streamlit interface, enter your Google Cloud API key.

4. Enter your API Key and choose a topic, set the difficulty, and start learning!

### Notes
- Ensure both the backend and frontend are running simultaneously.
- Keep your API key secure and do not share it publicly.
- You may need to adjust the `BASE_URL` in `frontend.py` if you're running the backend on a different port or host.

Enjoy learning with your Socratic Teaching Assistant!

### Authorship
This project, "Socratic Teaching Assistant for Data Structures and Algorithms," was developed by codename89.
