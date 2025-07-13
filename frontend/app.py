import requests
import streamlit as st

st.set_page_config(page_title="chat AI Agent", layout="centered")

st.title("Chat AI Agent")

# Backend API URL
API_URL = (
    "http://localhost:8000/chat"  # We can replace this URL with hosted backend url
)

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Chat UI functions
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


# Chat display area
st.markdown("---")
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.info("👋 Start a conversation by asking a question about Anything!")
    else:
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            if chat["role"] == "user":
                # User message - aligned right
                col1, col2 = st.columns([1, 3])
                with col2:
                    st.markdown(
                        f"""
                    <div style="
                        background-color: #0084ff;
                        color: white;
                        padding: 10px 15px;
                        border-radius: 15px;
                        margin: 5px 0;
                        text-align: left;
                        max-width: 80%;
                        margin-left: auto;
                        display: block;
                    ">
                        {chat['content']}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                # Assistant message - aligned left
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"""
                    <div style="
                        background-color: #f0f0f0;
                        color: #333;
                        padding: 10px 15px;
                        border-radius: 15px;
                        margin: 5px 0;
                        text-align: left;
                        max-width: 80%;
                        display: block;
                    ">
                        🤖 {chat['content']}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

# Input section at the bottom
st.markdown("---")

# Create columns for input and send button
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Message...",
        key="user_input",
        label_visibility="collapsed",
    )

with col2:
    send_clicked = st.button("Send", type="primary", use_container_width=True)

# Handle sending message
if send_clicked and user_input:
    handle_input(user_input)
    st.rerun()
