import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Learning Buddy - Arekapudi Hima Sree",
    page_icon="🎓"
)

# -----------------------------
# Initialize Gemini Model
# -----------------------------
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Cached AI Response Function
# -----------------------------
@st.cache_data(show_spinner=False)
def get_ai_response(prompt):

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:

            error_message = str(e)

            # Retry only if quota is exhausted
            if "429" in error_message or "Resource has been exhausted" in error_message:

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    return (
                        "⚠️ API quota exceeded.\n\n"
                        "Please wait a few minutes and try again."
                    )

            else:
                return f"❌ Error: {error_message}"

# -----------------------------
# App UI
# -----------------------------
st.title("🎓 AI Learning Buddy")
st.subheader("Created by Arekapudi Hima Sree")

topic = st.text_input("Enter a Topic")

option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Ask Anything"
    ]
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:

        if option == "Explain Concept":
            prompt = f"""
            You are a friendly AI tutor.

            Explain {topic} in simple language for beginners.

            Use:
            - Easy words
            - Short paragraphs
            - One real-life example
            """

        elif option == "Real-Life Example":
            prompt = f"""
            Give one simple real-life example of {topic}.
            Explain it step by step.
            """

        elif option == "Generate Quiz":
            prompt = f"""
            Create 5 multiple-choice questions on {topic}.

            Each question should have:
            - Four options (A, B, C, D)
            - Correct answer
            - Short explanation
            """

        else:
            prompt = topic

        with st.spinner("Generating response..."):
            answer = get_ai_response(prompt)

        st.success("Done!")
        st.write(answer)

