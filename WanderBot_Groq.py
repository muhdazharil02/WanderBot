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

Rewrite text to sound naturally written by a real person.

Main objective:
Make the text feel less structured, less polished, and less academic.

Rules:
- Use simple English.
- Use shorter sentences.
- Break long thoughts apart.
- Keep most sentences between 8 and 18 words.
- Add occasional very short sentences.
- Use contractions naturally.
- Use direct phrasing.
- Prefer verbs over noun-heavy wording.
- Keep flow uneven like normal human writing.
- Slight imperfections are acceptable.
- Vary sentence openings.
- Avoid repeating structure across paragraphs.
- Avoid sounding like a report or textbook.

Human writing patterns:
- Some paragraphs should be shorter.
- Some sentences should feel abrupt.
- Some transitions can be minimal.
- Not every sentence needs full explanation.
- Avoid over-connecting ideas.
- Avoid fully balanced arguments.
- Avoid overly smooth readability.

Strictly avoid:
- Academic tone
- Corporate tone
- Policy-writing tone
- Wikipedia style
- AI assistant tone
- Long compound sentences
- Long transition phrases
- High abstraction
- Excessive objectivity
- Repetitive paragraph patterns
- Multi-clause sentences
- Fancy synonyms
- Overly complete explanations

Avoid these words:
advent, paradigm, transformative,
moreover, furthermore, consequently,
therefore, necessitate, facilitate,
enhance, leverage, optimize,
substantial, significant, robust,
multidisciplinary, innovative,
implementation, integration,
operational, ethical concerns,
far-reaching, sophisticated,
numerous, various industries,
in modern society

Critical:
- Split ideas into smaller sentences.
- Reduce sentence complexity aggressively.
- Replace abstract wording with concrete wording.
- Sound closer to a student writing naturally.
- Do not sound like an academic article.
- Do not explain edits.
- Return only the rewritten text.
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
