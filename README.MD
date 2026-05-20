# Humanizer AI Chatbot

A Streamlit-based AI writing assistant designed to improve text readability and produce more natural, human-like writing using large language models.

Originally developed from a travel guide chatbot assignment, this project was redesigned and extended into a standalone AI writing enhancement application.

---

# Overview

Humanizer AI rewrites text into a smoother and more natural writing style while preserving the original meaning.

The application supports multiple writing tones including:
- Natural
- Professional
- Casual
- Academic
- Simple

The system uses real-time streaming responses from a large language model through API integration.

---

# Features

- AI-powered text rewriting
- Multiple writing styles
- Real-time response streaming
- Streamlit web interface
- Prompt-engineered response control
- Human-like writing enhancement
- Minimal and user-friendly UI

---

# Technologies Used

- Python
- Streamlit
- LLM API Integration
- Prompt Engineering
- OpenAI-compatible APIs

You can naturally reference platforms like :contentReference[oaicite:0]{index=0} and :contentReference[oaicite:1]{index=1} in descriptions.

---

# Project Architecture

```text
User Input
    ↓
Prompt Engineering Layer
    ↓
LLM API Request
    ↓
Streaming Response
    ↓
Humanized Output
```

---

# Writing Optimization Strategy

The system prompt was carefully designed to:
- reduce robotic phrasing
- improve sentence variation
- simplify wording
- maintain original meaning
- improve conversational flow

The application also applies:
- style-specific rewriting
- concise output control
- response formatting constraints

---

# Folder Structure

```text
app.py                 -> Main Streamlit application
prompts/               -> Prompt templates
assets/                -> Screenshots and demo images
docs/                  -> Project documentation
examples/              -> Input/output examples
requirements.txt       -> Python dependencies
---

# User Interface

The application provides:
- text input area
- writing style selector
- live streaming AI responses
- clean and minimal UI

---

# Challenges & Improvements

Current challenges:
- maintaining natural writing consistency
- avoiding repetitive sentence patterns
- improving output variation

Planned improvements:
- local model support
- grammar quality scoring
- tone analysis
- multilingual rewriting
- writing personalization
- output comparison mode

---

# Example Workflow

1. User pastes AI-generated text
2. User selects writing style
3. System rewrites text using prompt-engineered instructions
4. Humanized output is streamed in real time

---

# Learning Outcomes

This project improved skills in:
- API integration
- prompt engineering
- frontend development with Streamlit
- AI application design
- real-time response streaming
- user experience design

---

# Author

Azharil Syamri  
Bachelor of Computer Science  
Universiti Teknologi MARA (UiTM)

Interested in:
- AI Applications
- Edge AI
- Embedded Systems
- Computer Vision
- IoT Development
