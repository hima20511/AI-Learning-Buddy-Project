import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="AI Learning Buddy - Arekapudi Hima Sree",
    page_icon="🎓"
)

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

if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:

        if option == "Explain Concept":
            prompt = f"Explain {topic} in simple language for a beginner."

        elif option == "Real-Life Example":
            prompt = f"Give one simple real-life example of {topic}."

        elif option == "Generate Quiz":
            prompt = f"Create 5 multiple-choice questions on {topic} with answers."

        else:
            prompt = topic

        with st.spinner("Generating..."):
            response = model.generate_content(prompt)

        st.success("Done!")
        st.write(response.text)