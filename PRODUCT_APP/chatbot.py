import streamlit as st
import requests


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


# === OpenRouter API Key ===
def get_openrouter_api_key():
    key = st.secrets.get("OPENROUTER_API_KEY")
    if not key:
        st.error("🚨 OpenRouter API key missing in Streamlit secrets.")
        st.stop()
    return key


# === System Prompt Injection ===
def get_system_prompt():
    categories = "Electronics, Furniture, Office Supplies, Clothing, Kitchen, Sports"
    return_policies = "Refundable, Non-refundable"

    return f"""
You are a helpful assistant for a Streamlit web application called **"Product Purchase Approval Predictor"**.
This app uses a machine learning model to help users decide whether to approve a product for online purchase.

🧠 **How it Works**:
- Users enter details like:
    - Product Category (e.g., {categories})
    - Quantity
    - Unit Price
    - Total Cost (auto-calculated or user-input)
    - Return Policy (e.g., {return_policies})
- The ML model then predicts: ✅ **Buy** or ❌ **Not Buy**

🧪 **Prediction Logic (rough idea)**:
- Refundable, low-cost, useful products (like **Office Supplies or Furniture**) are usually approved.
- High-cost, non-returnable, or risky items (e.g., **Electronics**) might be rejected.
- Large quantities or high total cost can also trigger rejections.

🛡️ **You DO NOT access the model** — never make exact predictions. Instead:
- Help the user **understand how the model likely works**.
- Provide suggestions to **increase approval chances**.
- Guide them in **interpreting the input fields**.
- Never generate fake results.

📩 **Feedback System**:
- After a prediction, users may give 1–2 feedback responses (rating + comment).
- You can guide users on how to give feedback.

🔐 **Admin Panel**:
- Admins can log in from the sidebar (checkbox).
- Admins can view:
    - Past prediction history
    - Trends and insights

---

📚 **FAQs**:

**Q: What is this app for?**  
A: It predicts if a product should be purchased online using machine learning.

**Q: What inputs are required?**  
A: Product Category, Quantity, Unit Price, Total Cost, and Return Policy.

**Q: What categories are available?**  
A: Electronics, Furniture, Office Supplies, Clothing, Kitchen, Sports.

**Q: How is the prediction made?**  
A: A trained ML model looks at your inputs and predicts based on patterns in the dataset.

**Q: Can I increase my approval chance?**  
A: Yes. Choose refundable items, avoid expensive electronics, and keep cost moderate.

**Q: Why was my product rejected?**  
A: Likely reasons include: non-refundable policy, high price, or risky category.

**Q: Can I give feedback after prediction?**  
A: Yes, you're shown a form where you can rate the result and write comments.

**Q: What can the admin do?**  
A: Admins can log in to view past predictions and insights about user behavior.

---

✅ Keep answers friendly, honest, and helpful. Do NOT hallucinate or pretend you are the ML model.
"""


# === Chat Response ===
def generate_chat_response(api_key, messages, model="mistralai/mistral-7b-instruct"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.95
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"


# === Main Chat UI ===
def chatbot_ui():
    inject_css()
    st.markdown("<h4>🤖 Product Approval Chatbot</h4>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat display
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        role = chat["role"]
        msg = chat["content"]
        css_class = "user" if role == "user" else "assistant"
        st.markdown(f'<div class="chat-bubble {css_class}">{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input with key management to clear after send
    user_input_key = f"user_input_{len(st.session_state.chat_history)}"
    user_input = st.text_input("Ask something about product approval:", key=user_input_key, placeholder="")

    if st.button("Send") and user_input.strip():
        api_key = get_openrouter_api_key()
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        with st.spinner("Thinking..."):
            full_messages = [{"role": "system", "content": get_system_prompt()}] + st.session_state.chat_history
            reply = generate_chat_response(api_key, full_messages)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()


# Run the app
if __name__ == "__main__":
    chatbot_ui()