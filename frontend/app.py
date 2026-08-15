import streamlit as st
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="💬",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💬 Customer Support Chatbot")
st.markdown("Ask me anything about pricing, billing, account management, or technical support.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("About this chatbot")
st.sidebar.markdown("""
**How it works:**
1. You ask a question
2. The system searches our knowledge base using RAG
3. The answer is retrieved from real documentation
4. Sources are always shown — no hallucination possible

**Topics I can help with:**
- 💰 Pricing plans
- 💳 Billing and payments  
- 👤 Account management
- 🔧 Technical support
- ✨ Product features
- 🔒 Security and privacy
- 🚀 Getting started
- ❌ Cancellation policy
""")

# ── Check API health ──────────────────────────────────────────────────────────
try:
    health = requests.get(f"{API_URL}/health", timeout=3).json()
    st.sidebar.success(f"✅ API connected — {health['documents_indexed']} documents indexed")
except:
    st.sidebar.error("❌ API not connected — make sure FastAPI is running")

# ── Chat history ──────────────────────────────────────────────────────────────
# We store chat history in session state
# Session state persists across reruns within the same browser session
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your customer support assistant. How can I help you today?",
        "sources": [],
        "confidence": "high"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    confidence_color = (
                        "🟢" if source["relevance_score"] > 0.15
                        else "🟡" if source["relevance_score"] > 0.08
                        else "🔴"
                    )
                    st.write(
                        f"{confidence_color} **{source['title']}** "
                        f"(relevance: {source['relevance_score']:.3f})"
                    )

# ── Chat input ────────────────────────────────────────────────────────────────
# st.chat_input creates a chat input box at the bottom of the page
if question := st.chat_input("Ask a question..."):
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": question,
        "sources": []
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(question)
    
    # Get answer from API
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                    timeout=10
                )
                result = response.json()
                
                # Display answer
                st.write(result["answer"])
                
                # Show confidence indicator
                confidence = result["confidence"]
                score = result["confidence_score"]
                
                if confidence == "high":
                    st.success(f"✅ High confidence answer (score: {score:.3f})")
                elif confidence == "medium":
                    st.warning(f"⚠️ Medium confidence (score: {score:.3f}) — verify with support")
                else:
                    st.error(f"❌ Low confidence (score: {score:.3f}) — please contact support")
                
                # Show sources
                if result["sources"]:
                    with st.expander("📚 Sources used"):
                        for source in result["sources"]:
                            st.write(f"• **{source['title']}** — {source['category']}")
                
                # Show disclaimer
                st.caption(result["disclaimer"])
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                    "confidence": confidence
                })
                
            except Exception as e:
                error_msg = "Sorry, I couldn't connect to the knowledge base. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": [],
                    "confidence": "low"
                })

# ── Example questions ─────────────────────────────────────────────────────────
st.divider()
st.markdown("**Try asking:**")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("• How do I reset my password?")
    st.markdown("• What payment methods do you accept?")
with col2:
    st.markdown("• How do I cancel my subscription?")
    st.markdown("• Is my data GDPR compliant?")
with col3:
    st.markdown("• What does the Professional plan include?")
    st.markdown("• How do I enable two factor authentication?")