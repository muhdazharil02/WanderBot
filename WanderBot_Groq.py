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

Rewrite text so the writing sounds natural and human.

Core rules:
- Use simple wording.
- Use active voice.
- Keep sentences short to medium length.
- Mix sentence lengths naturally.
- Add occasional short sentences.
- Break long paragraphs into smaller ones.
- Sound slightly imperfect like real human writing.
- Keep flow natural, not overly polished.
- Preserve original meaning.
- Keep tone conversational and readable.

Human writing behavior:
- Some sentences should be extremely short.
- Some sentences can start with "And", "But", or "So".
- Avoid perfect structure.
- Avoid sounding like an essay generator.
- Avoid repeating sentence patterns.
- Reduce transition words.
- Use direct wording instead of academic wording.
- Prefer common words over advanced vocabulary.
- Use contractions when suitable.

Strictly avoid:
- Em dashes
- Semicolons
- Corporate tone
- Academic tone
- Overexplaining
- Repetitive transitions
- Balanced AI-style sentence structure
- Predictable paragraph patterns
- Fancy synonyms
- Long multi-clause sentences
- Excessive objectivity

Avoid these AI-style words:
advent, profound, myriad, permeating,
formidable, ephemeral, consequently,
furthermore, additionally, moreover,
leveraging, transformative, paradigm,
propensity, facilitating, enhancement,
significant, optimize, mitigate,
personalized, utilization, integration,
safeguarding, imperative, foster,
sustainable, unprecedented

Writing targets:
- Average sentence length around 10 to 18 words.
- Include occasional sentences under 8 words.
- Use simpler vocabulary.
- Sound like a student or normal writer.
- Do not sound like Wikipedia.
- Do not sound overly intelligent.
- Do not explain edits.
- Only return rewritten text.
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
