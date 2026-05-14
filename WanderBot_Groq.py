import streamlit as st
from openai import OpenAI

BASE_URL = "https://api.groq.com/openai/v1"
API_KEY = st.secrets["GROQ_API_KEY"]
# Better model for writing/humanizing
MODEL_NAME = "llama-3.3-70b-versatile"

# =========================
# PAGE
# =========================
st.set_page_config(page_title="Humanizer AI", page_icon="✍️")

st.title("✍️ Humanizer AI")
st.caption("By Azharil")

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_INSTRUCTION = """
You are Humanizer AI.

Rewrite the user's text so it sounds naturally written by a real person.

Guidelines:
- Make the writing conversational but professional.
- Use clear and simple language.
- Vary sentence lengths naturally.
- Mix short, medium, and longer sentences.
- Use smooth, natural transitions.
- Keep the flow human and readable.
- Preserve the original meaning.
- Keep the tone realistic and relaxed.
- Prefer common everyday wording.
- Use active voice.

Avoid:
- Robotic wording
- Predictable sentence patterns
- Academic or corporate tone
- Overly polished structure
- Repetitive transitions
- Fancy vocabulary
- Long multi-clause sentences
- AI-style phrasing
- Overexplaining

Do not:
- Explain changes
- Add commentary
- Add new information
- Use markdown
- Use em dashes

Return only the rewritten text.
"""
# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_INSTRUCTION
        }
    ]

# =========================
# TEXT INPUT
# =========================
st.subheader("Paste Your Text")

user_text = st.text_area(
    "Enter AI-generated text:",
    height=250,
    placeholder="Paste your text here..."
)

# Style options
style = st.selectbox(
    "Writing Style",
    [
        "Natural",
        "Professional",
        "Casual",
        "Academic",
        "Simple"
    ]
)

# =========================
# BUTTON
# =========================
if st.button("Humanize Text ✨"):

    if not user_text.strip():
        st.warning("Please paste some text first.")
        st.stop()

    # Add style instruction
    final_prompt = f"""
Rewrite the following text in a {style.lower()} human writing style.

TEXT:
{user_text}
"""

    st.session_state.messages.append({
        "role": "user",
        "content": final_prompt
    })

    try:
        client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY
        )

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            stream=True,
            temperature=0.9
        )

        st.subheader("Humanized Result")

        with st.chat_message("assistant"):
            response = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    except Exception as e:
        st.error("🚨 Error generating response")
        st.code(str(e))
