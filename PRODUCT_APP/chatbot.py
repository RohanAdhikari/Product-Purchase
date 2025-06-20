import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env at the very start
load_dotenv()

# === Inject Clean CSS ===
def inject_css():
    st.markdown("""
    <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f7f7f7;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
        }
        .chat-bubble {
            padding: 10px 14px;
            margin: 8px 0;
            border-radius: 12px;
            max-width: 90%;
            word-wrap: break-word;
            font-size: 15px;
        }
        .user {
            background-color: #1565c0;
            color: white;
            align-self: flex-end;
        }
        .assistant {
            background-color: #e0e0e0;
            color: black;
            align-self: flex-start;
        }
    </style>
    """, unsafe_allow_html=True)


# === Hugging Face API Key from .env ===
def get_huggingface_api_key():
    key = os.environ.get("HUGGINGFACE_API_KEY")
    if not key:
        st.error("🚨 Hugging Face API key is missing in .env or environment.")
        st.stop()
    return key.strip()


# === System Prompt Injection (Context for HuggingFace Prompt) ===
def get_system_prompt():
    categories = "Electronics, Furniture, Office Supplies, Clothing, Kitchen, Sports"
    return_policies = "Refundable, Non-refundable"
    return f"""
You are a helpful assistant for a Streamlit app called 'Product Purchase Approval Predictor'.
This app helps users decide if a product should be bought online.

The user will ask you questions about product approval prediction based on:
- Category (e.g. {categories})
- Quantity, Unit Price, Total Cost
- Return Policy (e.g. {return_policies})

Give helpful advice, guidance, and explanations. Do NOT make actual predictions.
"""


# === Chat Response from HuggingFace ===
def generate_chat_response(api_key, user_input, model="HuggingFaceH4/zephyr-7b-beta"):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = get_system_prompt() + "\nUser: " + user_input + "\nAssistant:"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "return_full_text": False
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        output = res.json()
        return output[0]["generated_text"].strip() if output else "⚠️ No response from model."
    except requests.exceptions.HTTPError as e:
        return f"⚠️ HTTP Error: {e} - Response: {res.text if res else 'No response'}"
    except Exception as e:
        return f"⚠️ Error: {e}"


# === Main Chat UI ===
def chatbot_ui():
    inject_css()
    st.markdown("<h4>🤖 Product Approval Chatbot</h4>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    api_key = get_huggingface_api_key()

    # Chat display
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        role = chat["role"]
        msg = chat["content"]
        css_class = "user" if role == "user" else "assistant"
        st.markdown(f'<div class="chat-bubble {css_class}">{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input field
    user_input_key = f"user_input_{len(st.session_state.chat_history)}"
    user_input = st.text_input("Ask something about product approval:", key=user_input_key, placeholder="")

    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        with st.spinner("Thinking..."):
            reply = generate_chat_response(api_key, user_input.strip())
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        st.rerun()


# Run the app directly (if standalone)
if __name__ == "__main__":
    chatbot_ui()
