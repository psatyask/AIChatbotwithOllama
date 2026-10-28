# 🤖 Ollama AI Chat Assistant

### A Local Generative AI Chat Application Built with Python, Streamlit & Ollama

A modern, ChatGPT-style conversational AI application powered by **locally hosted Large Language Models (LLMs)** using Ollama.

Built with Python and Streamlit, this project provides an interactive chat interface with real-time response streaming, conversation memory, customizable model settings, and support for multiple open-weight language models.

The application runs locally without requiring an OpenAI API key or paid API credits.

---

## ✨ Features

- **Modern Chat Interface:** Responsive dark-themed UI with a sidebar, welcome screen, and interactive chat components.
- **Local LLM Inference:** Run AI models directly on your computer using Ollama.
- **Real-Time Streaming:** Display model responses incrementally as they are generated.
- **Conversation Memory:** Maintain chat context using Streamlit Session State.
- **Dynamic Model Selection:** Automatically discover locally installed Ollama models.
- **Temperature Control:** Adjust model response variability between focused and creative outputs.
- **Custom System Prompts:** Configure the assistant's behavior and response style.
- **New Chat Functionality:** Clear conversation history and start fresh.
- **Example Prompts:** Quickly explore AI concepts, Python programming, and multilingual interactions.
- **Connection Monitoring:** Detect whether the Ollama server is available.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and API integration |
| Streamlit | Interactive web interface |
| Ollama | Local LLM inference and model management |
| REST API | Communication with the Ollama server |
| Requests | HTTP requests and response streaming |
| HTML & CSS | Custom styling and responsive UI |
| Streamlit Session State | Conversation history management |

## 🏗️ System Architecture

```text
           User
             |
             v
    Streamlit Web Interface
             |
             v
    Chat Input & Session State
             |
             v
     Ollama REST API
   localhost:11434/api/chat
             |
             v
     Local Language Model
    (Llama / Mistral / Qwen)
             |
             v
     Streaming AI Response
             |
             v
      Streamlit Chat UI
```

The application sends the configured system prompt and conversation history to the selected Ollama model. Responses are streamed back and displayed in the chat interface.

## 📂 Project Structure

```text
ollama-ai-chat/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore configuration
```

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have installed:

- Python 3.9 or newer
- Ollama
- pip
- Git (optional)

Ollama installation: https://ollama.com

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the example GitHub URL with your actual repository URL.

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install streamlit requests
```

Alternatively, create a `requirements.txt` file:

```text
streamlit
requests
```

Install using:

```bash
pip install -r requirements.txt
```

### 5. Start Ollama

If Ollama is not already running, start its local server:

```bash
ollama serve
```

Download a language model:

```bash
ollama pull llama3.2
```

You can also explore other models:

```bash
ollama pull mistral
ollama pull qwen2.5:3b
```

List installed models:

```bash
ollama list
```

### 6. Run the Application

```bash
streamlit run app.py
```

Open the application in your browser:

http://localhost:8501

## ⚙️ Model Configuration

Configure the assistant directly from the sidebar.

**Model Selection:** Choose from the language models installed on your computer.

**Temperature Control:**

| Temperature | Behavior |
|---|---|
| 0.0–0.3 | More focused and consistent |
| 0.4–0.7 | Balanced responses |
| 0.8–1.0 | More varied and creative |

**System Prompt:** Customize the assistant's behavior, such as:

```text
You are a helpful AI assistant specializing in
Python programming and machine learning.
Explain concepts in simple language and
provide practical examples.
```

## 🧠 How Conversation Memory Works

Language models do not automatically retain previous conversations across independent API requests.

This application implements conversation history using **Streamlit Session State**.

Each user message and successful assistant response is stored in:

```python
st.session_state.messages
```

For each request, the application sends:

1. System instructions
2. Previous user messages
3. Previous assistant responses
4. Current user message

This allows the model to generate context-aware replies.

Conversation history is maintained within the active Streamlit session and is not persisted in a database.

## ⚡ Real-Time Response Streaming

The application uses Ollama's chat API:

```text
POST http://localhost:11434/api/chat
```

Example payload:

```json
{
  "model": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "Explain Generative AI"
    }
  ],
  "stream": true,
  "options": {
    "temperature": 0.7
  }
}
```

Responses are processed incrementally and displayed with Streamlit's `st.write_stream()`.

This improves the user experience by displaying generated text before the full response is complete.

## 🔒 Privacy & Local Execution

The application communicates with a locally running Ollama server, allowing inference without sending prompts to a paid cloud-based LLM API.

Key considerations:

- No OpenAI API key is required.
- Model inference happens locally.
- Conversation history is stored in Streamlit session memory.
- Model downloads require internet access.
- Local execution does not automatically provide encryption, authentication, or persistent chat storage.

## 🛣️ Future Improvements

- [ ] Save and restore multiple conversations
- [ ] Add SQLite-based persistent chat history
- [ ] Support document upload and PDF question answering
- [ ] Implement Retrieval-Augmented Generation (RAG)
- [ ] Add conversational document search with vector embeddings
- [ ] Add model performance and token usage metrics
- [ ] Add chat export functionality
- [ ] Add authentication for multi-user access
- [ ] Support additional local AI models

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Integrating Large Language Models into Python applications
- Building interactive AI interfaces
- Working with REST APIs and streaming responses
- Managing conversational context
- Configuring local inference workflows
- Developing AI applications without relying on hosted LLM APIs

## 👨‍💻 Author

**Pardhu Satya Sai Krishna Alapati**

AI/ML Engineer | Generative AI | LLM Applications | Python

- **GitHub:** https://github.com/psatyask
- **Portfolio:** https://portifoli-9cde06110d13.herokuapp.com/

---

**Built with Python, Streamlit, and Ollama.**

*Exploring Generative AI through practical, locally deployed applications.*