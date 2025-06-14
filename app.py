"""
app.py – Streamlit UI for the Hybrid Modern RAG System
=======================================================
This file serves as the main entry point for the Streamlit application.
It assembles the UI from various modules located in the `ui`, `utils`,
and `state` directories.
"""
import streamlit as st
import os
from dotenv import load_dotenv

# ── Page Configuration (must be the first Streamlit command) ───────────────
st.set_page_config(
    page_title="RAG System • Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Load Environment & Modules ─────────────────────────────────────────────
load_dotenv()

try:
    from rag_system_enhanced import RAGSystem, Config
    from utils.style import STYLE
    from state import initialize_session_state, get_rag_system
    from ui.sidebar import render_sidebar, render_langsmith_info
    from ui.chat_tab import render_chat_tab
    from ui.dictionary_tab import render_dictionary_tab
    from ui.data_tab import render_data_tab
    from ui.documents_tab import render_documents_tab
    from ui.settings_tab import render_settings_tab
except ImportError as e:
    st.error(f"モジュールのインポートに失敗しました: {e}")
    st.error("必要なファイルが正しい場所にあるか確認してください。")
    st.stop()

# ── Apply Custom CSS ───────────────────────────────────────────────────────
st.markdown(STYLE, unsafe_allow_html=True)

# ── Environment Defaults ───────────────────────────────────────────────────
ENV_DEFAULTS = {
    "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY", ""),
    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
    "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", ""),
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", ""),
    "EMBEDDING_MODEL_IDENTIFIER": os.getenv("EMBEDDING_MODEL_IDENTIFIER", "text-embedding-ada-002"),
    "LLM_MODEL_IDENTIFIER": os.getenv("LLM_MODEL_IDENTIFIER", "gpt-4o"),
    "COLLECTION_NAME": os.getenv("COLLECTION_NAME", "documents"),
    "FINAL_K": int(os.getenv("FINAL_K", 5)),
    "ENABLE_JARGON_EXTRACTION": os.getenv("ENABLE_JARGON_EXTRACTION", "true").lower() == "true",
}

def main():
    """Main function to run the Streamlit application."""
    
    # ── Initialize State & RAG System ──────────────────────────────────────
    initialize_session_state()
    rag = get_rag_system()

    # ── Render Sidebar ─────────────────────────────────────────────────────
    render_langsmith_info()
    render_sidebar(rag, ENV_DEFAULTS)

    # ── Main Header ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1 class="header-title">iRAG</h1>
        <p class="header-subtitle">IHI's Smart Knowledge Base with SQL Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Main Tabs ──────────────────────────────────────────────────────────
    tab_titles = ["💬 Chat", "📖 Dictionary", "🗃️ Data", "📁 Documents", "⚙️ Settings"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        render_chat_tab(rag)
    
    with tabs[1]:
        render_dictionary_tab(rag)

    with tabs[2]:
        render_data_tab(rag)

    with tabs[3]:
        render_documents_tab(rag)

    with tabs[4]:
        render_settings_tab(rag, ENV_DEFAULTS)

if __name__ == "__main__":
    main()
