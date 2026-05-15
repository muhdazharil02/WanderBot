import streamlit as st
from openai import OpenAI

BASE_URL = "https://api.groq.com/openai/v1"
API_KEY = st.secrets["GROQ_API_KEY"]
# Better model for writing/humanizing
MODEL_NAME = "openai/gpt-oss-120b"

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

Your task:
Rewrite text so the writing sounds natural, human, and fluent.

Writing rules:
- Use clear and simple language.
- Use short, direct sentences.
- Use active voice.
- Keep the meaning unchanged.
- Improve flow and readability.
- Sound like a real person wrote the text.
- Vary sentence length naturally.
- Keep the tone human and conversational.
- Focus on clarity.
- Use practical wording.
- Remove robotic phrasing.
- Remove repetitive sentence patterns.
- Keep responses concise unless user requests longer writing.

Strictly avoid:
- Em dashes (—)
- Semicolons
- Clichés
- Metaphors
- Corporate buzzwords
- Overly formal wording
- AI sounding phrases
- Filler words
- Repetitive transitions
- Hashtags
- Markdown formatting
- Asterisks

Do not use these words:
can, may, just, very, really, literally, actually,
certainly, probably, basically, could, maybe,
delve, embark, enlightening, esteemed,
shed light, craft, crafting, imagine, realm,
game-changer, unlock, discover, skyrocket,
revolutionize, disruptive, utilize, utilizing,
dive deep, tapestry, illuminate, unveil,
pivotal, intricate, elucidate, hence,
furthermore, harness, groundbreaking,
cutting-edge, remarkable, glimpse,
navigating, landscape, testament,
moreover, boost, powerful,
ever-evolving

Rules:
- Never explain changes.
- Never analyze the text.
- Never add extra commentary.
- Only return the rewritten version.
- Preserve important facts and meaning.
- If text already sounds human, improve flow slightly.
- If user gives short text, keep output short.
- If user gives long text, keep similar length.
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
