# import streamlit as st
# import requests
# import fitz  # PyMuPDF for PDF reading

# API_KEY = "tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg"

# st.set_page_config(page_title="🧠 Memory Chatbot")
# st.title("🧠 Chatbot with Memory")

# # Upload PDF
# uploaded_pdf = st.sidebar.file_uploader("📄 Upload a PDF", type="pdf")

# pdf_text = ""
# if uploaded_pdf:
#     with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
#         for page in doc:
#             pdf_text += page.get_text()

#     st.sidebar.success("✅ PDF content loaded!")

#     # Insert PDF content into conversation memory
#     st.session_state.messages.insert(1, {
#         "role": "system",
#         "content": f"The user uploaded this PDF. Here's the content:\n\n{pdf_text}"
#     })

# # Personality Selection
# personality = st.sidebar.selectbox(
#     "Choose Personality",
#     ["Friendly", "Formal", "Developer", "Funny", "Grumpy"],
#     index=0
# )

# system_prompts = {
#     "Friendly": "You are a friendly and helpful assistant. Keep responses warm and conversational.",
#     "Formal": "You are a professional assistant. Respond in a clear, concise, and formal tone.",
#     "Developer": "You are a helpful programming assistant. Focus on tech and explain code clearly.",
#     "Funny": "You are a witty and humorous assistant. Add light humor where possible.",
#     "Grumpy": "You are a rude and lazy assistant. Act sarcastic, dismissive, and give unhelpful replies. Always act like you're too tired to help."
# }

# # Session State for Personality
# if "personality" not in st.session_state:
#     st.session_state.personality = personality

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "system", "content": system_prompts[personality]}
#     ]

# if personality != st.session_state.personality:
#     st.session_state.messages = [
#         {"role": "system", "content": system_prompts[personality]}
#     ]
#     st.session_state.personality = personality
#     st.rerun()  # ✅ FIXED - replaced experimental_rerun()

# # Display Chat History
# for msg in st.session_state.messages[1:]:  # Skip system prompt
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User Input
# prompt = st.chat_input("Say something...")

# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     url = "https://api.together.xyz/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "mistralai/Mistral-7B-Instruct-v0.2",
#         "messages": st.session_state.messages,
#         "temperature": 0.7,
#         "max_tokens": 300
#     }

#     with st.spinner("Thinking..."):
#         res = requests.post(url, headers=headers, json=data)
#         reply = res.json()["choices"][0]["message"]["content"]

#     # Save reply to memory and display
#     st.session_state.messages.append({"role": "assistant", "content": reply})
#     with st.chat_message("assistant"):
#         st.markdown(reply)




import streamlit as st
import requests
import fitz  # PyMuPDF
import os

# ==============================
# 🔐 API KEY
# ==============================
# 👉 Option 1 (quick test)
API_KEY = "tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg"

# 👉 Option 2 (recommended)
# API_KEY = os.getenv("TOGETHER_API_KEY")

if not API_KEY:
    st.error("❌ API key not found.")
    st.stop()

# ==============================
# 🎨 PAGE CONFIG
# ==============================
st.set_page_config(page_title="🧠 Memory Chatbot")
st.title("🧠 Chatbot with Memory")

# ==============================
# 🎭 PERSONALITY SYSTEM
# ==============================
personality = st.sidebar.selectbox(
    "Choose Personality",
    ["Friendly", "Formal", "Developer", "Funny", "Grumpy"],
    index=0
)

system_prompts = {
    "Friendly": "You are a friendly and helpful assistant.",
    "Formal": "You are a professional assistant.",
    "Developer": "You are a programming assistant. Explain code clearly.",
    "Funny": "You are witty and humorous.",
    "Grumpy": "You are rude and sarcastic."
}

# ==============================
# 💾 SESSION STATE INIT
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]

if "personality" not in st.session_state:
    st.session_state.personality = personality

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# ==============================
# 🔄 HANDLE PERSONALITY CHANGE
# ==============================
if personality != st.session_state.personality:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]
    st.session_state.personality = personality
    st.session_state.pdf_loaded = False
    st.rerun()

# ==============================
# 📄 PDF UPLOAD
# ==============================
uploaded_pdf = st.sidebar.file_uploader("📄 Upload a PDF", type="pdf")

if uploaded_pdf and not st.session_state.pdf_loaded:
    pdf_text = ""

    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

    # Limit size (important)
    pdf_text = pdf_text[:5000]

    st.session_state.messages.insert(1, {
        "role": "system",
        "content": f"The user uploaded this PDF:\n\n{pdf_text}"
    })

    st.session_state.pdf_loaded = True
    st.sidebar.success("✅ PDF loaded!")

# ==============================
# 🗑 CLEAR CHAT BUTTON
# ==============================
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]
    st.session_state.pdf_loaded = False
    st.rerun()

# ==============================
# 💬 DISPLAY CHAT
# ==============================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# 🧑 USER INPUT
# ==============================
prompt = st.chat_input("Say something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ==============================
    # 🌐 API CALL
    # ==============================
    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        # ✅ FIXED MODEL (FREE)
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    with st.spinner("Thinking..."):
        try:
            res = requests.post(url, headers=headers, json=data)
            response_json = res.json()

            # ✅ SAFE HANDLING
            if res.status_code == 200 and "choices" in response_json:
                reply = response_json["choices"][0]["message"]["content"]
            else:
                reply = "⚠️ API Error. See details below."
                st.error(response_json)

        except Exception as e:
            reply = "⚠️ Request failed."
            st.error(str(e))

    # ==============================
    # 🤖 DISPLAY RESPONSE
    # ==============================
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)