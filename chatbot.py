# tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg
import streamlit as st
import requests


API_KEY = "tgp_v1_O2Xw6iZvD3rf4JVgxDG1A4uvnV0zpKPAaVOJ9wAR3Mg"

st.set_page_config(page_title="🧠 Memory Chatbot")
st.title("🧠 Chatbot with Memory")


uploaded_pdf = st.sidebar.file_uploader("📄 Upload a PDF", type="pdf")

pdf_text = ""
if uploaded_pdf:
    import fitz 
    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()

    st.sidebar.success("PDF content loaded!")

   
    st.session_state.messages.insert(1, {
        "role": "system",
        "content": f"The user uploaded this PDF. Here's the content:\n\n{pdf_text}"
    })
personality = st.sidebar.selectbox(
    "Choose Personality",
    ["Friendly", "Formal", "Developer", "Funny", "Grumpy" ],
    index=0
)

system_prompts = {
    "Friendly": "You are a friendly and helpful assistant. Keep responses warm and conversational.",
    "Formal": "You are a professional assistant. Respond in a clear, concise, and formal tone.",
    "Developer": "You are a helpful programming assistant. Focus on tech and explain code clearly.",
    "Funny": "You are a witty and humorous assistant. Add light humor where possible.",
    "Grumpy": "You are a rude and lazy assistant. Act sarcastic, dismissive, and give unhelpful or annoying replies. Always act like you're too tired to help.",
   
}


if "personality" not in st.session_state:
    st.session_state.personality = personality

if personality != st.session_state.personality:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]
    st.session_state.personality = personality
    st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompts[personality]}
    ]


for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Say something...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    with st.spinner("Thinking..."):
        res = requests.post(url, headers=headers, json=data)
        reply = res.json()["choices"][0]["message"]["content"]

    # Save reply to memory and display
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
