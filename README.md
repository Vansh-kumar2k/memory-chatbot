<div align="center">

# 🧠 MemoryChat

### *A context-aware AI chatbot with switchable personalities and PDF document understanding — powered by Mistral 7B.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Mistral 7B](https://img.shields.io/badge/Mistral-7B_Instruct_v0.2-6366F1?style=flat-square)](https://mistral.ai)
[![Together AI](https://img.shields.io/badge/Together.ai-API-0EA5E9?style=flat-square)](https://together.xyz)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

</div>

---

## 🚀 Product Overview

**MemoryChat** is a Streamlit-based AI chatbot that maintains full conversation memory across a session, understands uploaded PDF documents, and adapts its tone through five distinct personality modes — all powered by **Mistral 7B Instruct** via the Together AI API.

Unlike stateless chatbots, MemoryChat carries the entire conversation history in every API request, giving the model full context to reason, recall, and respond intelligently.

> Upload a research paper, switch to Developer mode, and ask it to summarize the algorithm. MemoryChat just gets it.

---

## ✨ Features

- 🧠 **Persistent Conversation Memory** — Full chat history is passed on every request; the model remembers everything said in the session
- 📄 **PDF Document Upload** — Upload any PDF and chat about its contents; text is extracted and injected into the conversation context
- 🎭 **5 Personality Modes** — Switch between Friendly, Formal, Developer, Funny, and Grumpy personas; context resets automatically on switch
- ⚡ **Mistral 7B Instruct** — Fast, capable open-source LLM served via Together AI's inference API
- 🖥️ **Streamlit UI** — Clean, zero-config web interface with sidebar controls and native chat bubbles
- 🔄 **Live Personality Switching** — Changing personality instantly resets the system prompt and reruns the app

---

## 🎭 Personality Modes

| Mode | Behavior |
|---|---|
| 😊 **Friendly** | Warm, conversational, helpful — great for everyday use |
| 👔 **Formal** | Professional, concise, structured — ideal for work tasks |
| 💻 **Developer** | Tech-focused, explains code clearly — built for engineers |
| 😄 **Funny** | Witty and humorous — lightens the mood |
| 😤 **Grumpy** | Sarcastic and dismissive — for when you need a challenge |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **UI Framework** | Streamlit |
| **LLM** | Mistral 7B Instruct v0.2 |
| **Inference API** | Together AI (`/v1/chat/completions`) |
| **PDF Parsing** | PyMuPDF (`fitz`) |
| **State Management** | Streamlit `session_state` |
| **Language** | Python 3.10+ |

---

## 📁 Project Structure

```
memorychat/
├── app.py              # Main Streamlit app — chat logic, PDF upload, personality switching
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed)
└── README.md
```

---

## 🎬 Demo

<div align="center">

https://github.com/your-username/memorychat/assets/your-user-id/your-video-file.mp4

> 💡 *To embed a demo video on GitHub: drag and drop your `.mp4` file into any GitHub Issue comment box → copy the generated URL → paste it above, replacing the placeholder link.*

</div>

---

## 📸 Screenshots

<div align="center">

**Chat Interface with Memory**
![Chat Interface](assets/screenshot-chat.png)

**PDF Upload & Document Q&A**
![PDF Upload](assets/screenshot-pdf.png)

</div>

> 💡 *To add screenshots: create an `assets/` folder in your repo, add your images named `screenshot-chat.png` and `screenshot-pdf.png`, and they will appear here automatically.*

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- A valid [Together AI API key](https://together.xyz)
- `pip` and `virtualenv`

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/memorychat.git
cd memorychat
```

### 2. Create & Activate a Virtual Environment

```bash
# Create virtualenv
python -m venv venv

# Activate — macOS/Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` should include:**
```
streamlit
requests
pymupdf
python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TOGETHER_API_KEY=your_together_api_key_here
```

Then update `app.py` to load it securely:

```python
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("TOGETHER_API_KEY")
```

> 🔐 **Never hardcode your API key.** Always use `.env` and add it to `.gitignore`.

### 5. Run the App

```bash
streamlit run app.py
```

The app will open automatically at **[http://localhost:8501](http://localhost:8501)**

---

## 🔗 LLM API Reference

MemoryChat calls the Together AI chat completions endpoint directly:

**Endpoint:**
```
POST https://api.together.xyz/v1/chat/completions
```

**Request Payload:**
```json
{
  "model": "mistralai/Mistral-7B-Instruct-v0.2",
  "messages": [
    { "role": "system", "content": "You are a friendly assistant..." },
    { "role": "user",   "content": "Hello!" },
    { "role": "assistant", "content": "Hi there! How can I help?" },
    { "role": "user",   "content": "What did I just say?" }
  ],
  "temperature": 0.7,
  "max_tokens": 300
}
```

**Key design decision:** The entire `st.session_state.messages` list — including system prompt, PDF context, and full chat history — is sent on every request. This is what gives the model its "memory."

---

## 📄 How PDF Context Works

1. User uploads a `.pdf` via the sidebar file uploader
2. PyMuPDF (`fitz`) extracts all text from every page
3. The extracted text is injected as a `system` message at position `[1]` in the message history
4. All subsequent chat turns are aware of the PDF content
5. Users can then ask questions, request summaries, or query specific sections

```python
st.session_state.messages.insert(1, {
    "role": "system",
    "content": f"The user uploaded this PDF. Here's the content:\n\n{pdf_text}"
})
```

---

## 🧪 Testing

```bash
pip install pytest
pytest tests/
```

**Recommended test scenarios:**

- Chat with memory: ask the bot to recall something said earlier in the session
- PDF upload: upload a PDF, then ask a question specific to its content
- Personality switch: verify that switching personality resets the message history
- API error handling: simulate a failed Together AI request

---

## 🚀 Deployment

### Deploy to Streamlit Cloud (Recommended — Free)

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New App
3. Select your repo and set `app.py` as the entry point
4. Add `TOGETHER_API_KEY` under **Secrets** in the Streamlit dashboard
5. Deploy 🎉

### Deploy to Hugging Face Spaces

1. Create a new Space → select **Streamlit** as the SDK
2. Push your code to the Space repo
3. Add your API key under **Settings → Repository Secrets**

### Deploy with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t memorychat .
docker run -p 8501:8501 --env-file .env memorychat
```

---

## 🛣️ Roadmap

- [ ] 🔐 Secure API key loading via `.env` (security hardening)
- [ ] 🗂️ Multi-PDF upload and document switching
- [ ] 💾 Export chat history as `.txt` or `.pdf`
- [ ] 🌐 Model selector — switch between Mistral, LLaMA 3, Gemma, etc.
- [ ] 🔢 Token usage tracker and context window indicator
- [ ] 🧵 Named conversation sessions with save/load
- [ ] 🔊 Voice input via browser speech API

---

## 🤝 Contributing

Contributions are warmly welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow existing code style and add comments where relevant.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.

---

<div align="center">

Built with ❤️ using Streamlit & Mistral 7B · Powered by Together AI

*Star ⭐ this repo if MemoryChat helped you build something awesome!*

</div>
