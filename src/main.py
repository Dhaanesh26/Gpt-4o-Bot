import os
import json
import streamlit as st
import openai  # Import the OpenAI library

# Load the API key from a config file
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

# Load configuration data
with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

OPENAI_API_KEY = config_data["OPENAI_API_KEY"]

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Configure Streamlit page settings
st.set_page_config(
    page_title="GPT-4 Chat",
    page_icon="💬"
)

# Initialize chat session in Streamlit if not present already
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit page title
st.title("🖥️ Gen-AI GPT-4 Chat")

# Display chat history
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for the user's message
user_prompt = st.chat_input("Ask Gen AI GPT-4 Chat")

if user_prompt:
    # Add user's message to chat history and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state["chat_history"].append({"role": "user", "content": user_prompt})

    # Send user's message to GPT-4 and get a response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state["chat_history"]
            ]
        )

        # Extract GPT-4's response
        assistant_response = response['choices'][0]['message']['content']
        st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})

        # Display GPT-4's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"An error occurred: {e}")


