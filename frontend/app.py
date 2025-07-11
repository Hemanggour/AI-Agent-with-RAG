import streamlit as st
import requests

st.set_page_config(page_title="Accounting AI Assistant", layout="centered")

st.title("Accounting AI Assistant")
st.markdown("Ask anything about Indian Accounting Standards (IND AS)")

# Backend API URL
API_URL = "http://localhost:8000/chat"  # We can replace this URL with hosted backend url


# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Chat UI
def send_message(user_input):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    try:
        res = requests.post(API_URL, json={"message": user_input})
        res.raise_for_status()
        bot_reply = res.json()["response"]
    except Exception as e:
        bot_reply = f"Error: {e}"
    
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

def handle_input(user_input):
    if user_input:
        send_message(user_input)
        st.session_state.input = ""


# Text input field
user_input = st.text_input("Your question", key="user_input")

if st.button("Send"):
    handle_input(user_input)


# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Assistant:** {chat['content']}")
