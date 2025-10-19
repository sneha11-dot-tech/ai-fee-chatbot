import streamlit as st
from chatbot import generate_answer

# Page configuration
st.set_page_config(page_title="AI Fee Query Chatbot", page_icon="💬")
st.title("💬 AI Fee Query Chatbot for College Fees")

# Session state to keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Function to handle user input
def send_message():
    user_msg = st.session_state.user_input.strip()
    if user_msg == "":
        return
    st.session_state.history.append(("You", user_msg))
    bot_reply = generate_answer(user_msg)
    st.session_state.history.append(("Bot", bot_reply))
    st.session_state.user_input = ""  # clear input box

# Input box
st.text_input(
    "Type your question here (e.g., 'What is the admission fee for BCA?')",
    key="user_input",
    on_change=send_message
)

st.markdown("---")

# Display chat history (latest at top)
for speaker, msg in st.session_state.history[::-1]:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")
