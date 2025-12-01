import streamlit as st
from openai import OpenAI

BASE_URL = "https://api.groq.com/openai/v1"
API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "openai/gpt-oss-120b"


# --- App Interface ---
st.set_page_config(page_title="WanderBot", page_icon="✈️")
st.title("✈️ WanderBot")
st.caption(f"Powered by Groq Cloud ({MODEL_NAME}) - Super Fast ⚡")

# --- Persona ---
SYSTEM_INSTRUCTION = """
You are WanderBot, a helpful and efficient virtual travel agent.
1. Help users find hotels, activities, and travel tips.
2. Be concise and use bullet points for recommendations.
3. If asked about non-travel topics, politely redirect to travel planning.
"""

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "assistant", "content": "Hello! I am ready to help you plan your trip."}
    ]

# --- Display Chat ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Ask about destinations..."):
    
    # 1. Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Generate Response with STREAMING
    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        
        # We enable stream=True here
        stream = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=st.session_state.messages,
            stream=True  # <--- This enables the typing effect
        )
        
        # 3. Stream the output to the UI
        with st.chat_message("assistant"):
            # st.write_stream is a magic Streamlit command that handles the generator automatically
            response = st.write_stream(stream)
        
        # 4. Save the final full response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error("🚨 Connection Error!")
        st.code(str(e))