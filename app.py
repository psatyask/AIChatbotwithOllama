
import json
import requests
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ollama AI | Local Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Explain concepts clearly "
    "and simply. When useful, provide examples."
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ============================================================
# OLLAMA HELPERS
# ============================================================

def check_ollama_running():
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=3
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_installed_models():
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )
        response.raise_for_status()

        models = response.json().get("models", [])

        return [model["name"] for model in models]

    except (requests.exceptions.RequestException, ValueError, KeyError):
        return []


def stream_ollama_response(model, messages, temperature):
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature
        }
    }

    with requests.post(
        OLLAMA_CHAT_URL,
        json=payload,
        stream=True,
        timeout=300
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line.decode("utf-8"))

            if chunk.get("error"):
                raise RuntimeError(chunk["error"])

            content = chunk.get("message", {}).get("content", "")

            if content:
                yield content

            if chunk.get("done", False):
                break


# ============================================================
# CUSTOM CSS - MODERN DARK AI THEME
# ============================================================

st.markdown("""
<style>

:root {
    --background: #0b0f14;
    --sidebar: #10161e;
    --surface: #151d27;
    --surface-hover: #1d2935;
    --border: #293442;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --accent: #22c55e;
    --accent-hover: #16a34a;
}

/* MAIN APPLICATION */

.stApp {
    background: var(--background);
    color: var(--text);
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] hr {
    border-color: var(--border);
}

/* LOGO */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0 16px;
}

.sidebar-logo {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #22c55e, #15803d);
    border-radius: 13px;
    font-size: 24px;
}

.sidebar-title {
    color: #f8fafc;
    font-size: 19px;
    font-weight: 750;
}

.sidebar-caption {
    color: #94a3b8;
    font-size: 12px;
}

/* TOP HEADER */

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0 24px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

.app-title {
    font-size: 19px;
    font-weight: 750;
    color: #f8fafc;
}

.app-description {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
}

.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(34,197,94,0.3);
    background: rgba(34,197,94,0.08);
    padding: 8px 14px;
    border-radius: 30px;
    font-size: 12px;
    color: #86efac;
    font-weight: 600;
}

/* WELCOME SCREEN */

.welcome-container {
    text-align: center;
    padding: 65px 0 28px;
}

.welcome-icon {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 76px;
    height: 76px;
    background: linear-gradient(135deg, #14532d, #166534);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 24px;
    font-size: 36px;
    margin-bottom: 24px;
    box-shadow: 0 15px 50px rgba(34,197,94,0.12);
}

.welcome-title {
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    letter-spacing: -1.3px;
    margin-bottom: 12px;
    color: #f8fafc;
}

.welcome-title span {
    color: #4ade80;
}

.welcome-description {
    font-size: 15px;
    line-height: 1.8;
    color: #94a3b8;
    max-width: 520px;
    margin: 0 auto;
}

.suggestion-heading {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-top: 22px;
    padding-bottom: 10px;
}

/* BUTTONS */

.stButton > button {
    border-radius: 13px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: #e2e8f0;
    font-weight: 550;
    min-height: 48px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #22c55e;
    background: var(--surface-hover);
    color: #86efac;
}

.stButton > button:focus {
    color: #f8fafc;
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    border: 1px solid #25313f;
    border-radius: 17px;
    padding: 18px 20px;
    margin-bottom: 14px;
    background: #121a24;
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #17251d;
    border-color: #24543a;
}

[data-testid="stChatMessage"] p {
    line-height: 1.8;
    font-size: 15px;
}

/* INPUT */

[data-testid="stChatInput"] {
    border-radius: 16px;
}

[data-testid="stChatInput"] > div {
    background: #18212b;
    border: 1px solid #344153;
    border-radius: 16px;
}

[data-testid="stChatInput"] textarea {
    color: #f8fafc;
}

[data-testid="stChatInput"] button {
    color: #4ade80;
}

/* SIDEBAR LABELS */

.stSelectbox label,
.stSlider label,
.stTextArea label {
    font-weight: 600;
    color: #e2e8f0;
}

/* SMALL TEXT */

.status-online {
    color: #4ade80;
    font-size: 13px;
    font-weight: 600;
}

.status-offline {
    color: #f87171;
    font-size: 13px;
    font-weight: 600;
}

.section-label {
    font-size: 12px;
    font-weight: 750;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 18px 0 12px;
}

.info-note {
    color: #94a3b8;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 12px;
}

.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 22px;
    padding-bottom: 10px;
}

/* HIDE EXTRA STREAMLIT ELEMENTS */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* RESPONSIVE */

@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .welcome-container {
        padding-top: 30px;
    }

    .welcome-title {
        font-size: 28px;
    }

    .app-header {
        gap: 12px;
    }

    .model-badge {
        font-size: 10px;
        padding: 6px 9px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# OLLAMA CONNECTION
# ============================================================

ollama_online = check_ollama_running()

installed_models = get_installed_models() if ollama_online else []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🤖</div>
        <div>
            <div class="sidebar-title">Ollama AI</div>
            <div class="sidebar-caption">Your Local AI Workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if ollama_online:
        st.markdown(
            '<div class="status-online">● Ollama Connected</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-offline">● Ollama Offline</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-label">Model Configuration</div>',
        unsafe_allow_html=True
    )

    if installed_models:

        model_names = installed_models

        if st.session_state.selected_model not in model_names:
            st.session_state.selected_model = model_names[0]

        model = st.selectbox(
            "AI Model",
            model_names,
            key="selected_model",
            help="Models currently installed in your Ollama environment."
        )

    else:
        model = st.selectbox(
            "AI Model",
            [
                "llama3.2",
                "llama3.1",
                "mistral",
                "gemma2",
                "qwen2.5"
            ],
            index=0,
            disabled=True,
            help="Connect Ollama to load installed models."
        )

    st.slider(
        "Creativity / Temperature",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        key="temperature",
        help="Lower values produce more focused answers. Higher values allow more variation."
    )

    st.markdown(
        '<div class="section-label">Assistant Instructions</div>',
        unsafe_allow_html=True
    )

    st.text_area(
        "System Prompt",
        key="system_prompt",
        height=135,
        help="Customize the assistant's behavior."
    )

    st.divider()

    st.markdown(
        '<div class="section-label">Conversation</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋  New Chat",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    message_count = len(st.session_state.messages)

    st.caption(f"💬 {message_count} messages in current conversation")

    st.divider()

    st.markdown(
        '<div class="section-label">About This Project</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    **Tech Stack**
    
    - Python
    - Streamlit
    - Ollama
    - Local Large Language Models
    
    **Features**
    
    - Real-time streaming
    - Conversation memory
    - Temperature control
    - Custom system instructions
    - Dynamic model selection
    """)

    st.markdown(
        '<div class="info-note">'
        '🔒 Local inference — no OpenAI API key required.'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

selected_model = st.session_state.selected_model

safe_model_name = (
    selected_model
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
    .replace('"', "&quot;")
)

st.markdown(f"""
<div class="app-header">
    <div>
        <div class="app-title">Ollama AI Assistant</div>
        <div class="app-description">
            Your private workspace powered by local AI
        </div>
    </div>
    <div class="model-badge">
        ● {safe_model_name}
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# OFFLINE HANDLING
# ============================================================

if not ollama_online:

    st.error("Ollama is not running or cannot be reached.")

    st.markdown("Start Ollama using the following command:")

    st.code("ollama serve", language="bash")

    st.info(
        "If the Ollama desktop application is already running, "
        "check that its local API is available at "
        "http://localhost:11434"
    )

    if st.button("↻ Recheck Connection"):
        st.rerun()

    st.stop()


if not installed_models:

    st.warning("No installed Ollama models were found.")

    st.code("ollama pull llama3.2", language="bash")

    st.stop()


# ============================================================
# WELCOME SCREEN
# ============================================================

# ============================================================
# WELCOME SCREEN
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
<div class="welcome-container">
    <div class="welcome-icon">✦</div>
    <div class="welcome-title">
        Your AI. <span>Your Machine.</span>
    </div>
    <div class="welcome-description">
        Experience the power of generative AI directly
        on your laptop. Ask questions, explore ideas,
        write code, and learn new concepts using
        locally running language models.
    </div>
</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="suggestion-heading">Try asking something</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:

        if st.button(
            "🧠  Explain Generative AI",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain Generative AI in simple terms with examples."
            )

        if st.button(
            "🐍  Learn Python Programming",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Teach me Python programming from the basics."
            )

    with col2:

        if st.button(
            "💻  Write Python Code",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Write a Python program to demonstrate "
                "a simple machine learning model."
            )

        if st.button(
            "🌍  Explain AI in Telugu",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Generative AI ante enti? "
                "Explain in simple Telugu-English."
            )

    st.markdown("""
    <div class="footer-note">
        Powered by Ollama • Runs Locally • Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "Message Ollama AI...",
    disabled=not ollama_online
)

# Handle clickable suggestion prompts
if st.session_state.pending_prompt:

    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# ============================================================
# CHAT PROCESSING
# ============================================================

if user_prompt:

    # Add user message to conversation memory
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Build messages for Ollama
    messages_for_ollama = [
        {
            "role": "system",
            "content": st.session_state.system_prompt
        }
    ]

    messages_for_ollama.extend(st.session_state.messages)

    # Display streamed assistant response
    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                full_response = st.write_stream(
                    stream_ollama_response(
                        model=st.session_state.selected_model,
                        messages=messages_for_ollama,
                        temperature=st.session_state.temperature
                    )
                )

            # Save successful response to memory
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except requests.exceptions.HTTPError as error:

            st.error(
                f"Ollama HTTP Error: {error}. "
                "Check that the selected model is available."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Connection error: {error}. "
                "Check your Ollama server."
            )

        except (ValueError, RuntimeError) as error:

            st.error(f"Model response error: {error}")

    st.rerun()
