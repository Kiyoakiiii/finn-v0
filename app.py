from pathlib import Path

import streamlit as st

from finn.agent import FinnAgent
from finn.user_context import load_user_profile


ROOT = Path(__file__).parent
KB_PATH = ROOT / "data" / "knowledge_base.md"
PROFILE_PATH = ROOT / "data" / "sample_user_profile.json"


@st.cache_resource
def get_agent() -> FinnAgent:
    return FinnAgent(kb_path=KB_PATH, user_profile_path=PROFILE_PATH)


st.set_page_config(page_title="Finn v0", page_icon="F", layout="centered")

agent = get_agent()
profile = load_user_profile(PROFILE_PATH)

st.title("Finn")
st.caption("A v0 wellness assistant for fini")

with st.sidebar:
    st.header("Sample app context")
    st.write(f"Goal: {profile.primary_goal}")
    st.write(f"Sleep avg: {profile.avg_sleep_hours} hours")
    st.write(f"Stress: {profile.stress_level}/10")
    st.write(f"Hydration: {profile.daily_water_cups} cups/day")
    st.write(f"Activity: {profile.activity_level}")
    st.divider()
    st.caption("This prototype uses local sample data only.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I am Finn. Ask me about sleep, stress, hydration, movement, nutrition, or habit building.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask Finn a wellness question")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = agent.answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer.response})

    with st.chat_message("assistant"):
        st.markdown(answer.response)
        if answer.sources:
            with st.expander("Sources used"):
                for source in answer.sources:
                    st.markdown(f"**{source.title}**")
                    st.caption(source.snippet)
