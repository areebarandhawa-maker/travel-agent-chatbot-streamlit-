
from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL = "openai/gpt-oss-120b"

SYSTEM = (
    "You are Travel agent, a friendly and helpful travel assistant. "
    "Only talk about travel and tourism. "
    "Help users with travel destinations, trip planning, itineraries, "
    "hotels, transportation, budgets, sightseeing, local culture, "
    "food recommendations while traveling, and travel tips. "
    "Ask clarifying questions when needed. "
    "Provide practical, clear, and friendly answers. "
    "Do not answer questions unrelated to travel and tourism. "
    "Do not invent booking confirmations, prices, or availability."
)

st.set_page_config(
    page_title="Travel agent - Your Friendly Travel Assistant",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Travel agent - Your Friendly Travel Assistant")
st.caption("Ask me anything about travel, destinations, and trip planning!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM}
    ]

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

user_text = st.chat_input(
    "Where would you like to travel?"
)

if user_text:
    st.session_state.messages.append({
        "role": "user",
        "content": user_text
    })

    with st.chat_message("user"):
        st.write(user_text)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Planning your next adventure..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    max_tokens=500,
                    temperature=0.7,
                )

                reply = response.choices[0].message.content

            st.write(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:
        st.error(f"Something went wrong: {e}")

with st.sidebar:
    st.header("🌍 Travel agent")
    st.write("Your personal travel planning assistant.")
    st.markdown("### Try asking:")
    st.markdown("- Plan a 5-day trip to Turkey")
    st.markdown("- Best places to visit in Pakistan")
    st.markdown("- Suggest a budget trip to Dubai")
    st.markdown("- Create a honeymoon itinerary")
    st.markdown("- What should I pack for a trip?")
    
    if st.button("Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM}
        ]
        st.rerun()
