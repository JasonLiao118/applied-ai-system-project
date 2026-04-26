import os
import streamlit as st
from dotenv import load_dotenv
from password_bot import PasswordBot
from llm_client import GeminiClient

load_dotenv()

st.set_page_config(page_title="Password Evaluator", page_icon="🔐")
st.title("🔐 AI Password Evaluator")
st.caption("Enter a password and the AI will judge its strength against local security criteria.")

# ------------------------------------------------------------------
# Session state defaults
# ------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None

# ------------------------------------------------------------------
# User controls
# ------------------------------------------------------------------
st.subheader("Your Password")

show_password = st.checkbox("Show password", value=False)
password_input = st.text_input(
    "Enter a password to evaluate",
    type="default" if show_password else "password",
    placeholder="Type or paste your password here…",
)

purpose = st.selectbox(
    "What is this password for?",
    [
        "General",
        "Banking / Financial",
        "Social Media",
        "Work / Enterprise",
        "WiFi / Network",
        "PIN / Numeric",
        "High Security / Passphrase",
    ],
)

user_params = {"purpose": purpose}

evaluate_btn = st.button("Evaluate Password 🔍", type="primary")

# ------------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------------
if evaluate_btn:
    if not os.getenv("GEMINI_API_KEY"):
        st.error("GEMINI_API_KEY not found. Add it to your .env file and restart the app.")
    elif not password_input:
        st.error("Enter a password to evaluate.")
    else:
        try:
            with st.spinner("Retrieving security criteria and evaluating…"):
                llm = GeminiClient()
                bot = PasswordBot(llm_client=llm)
                result = bot.evaluate_password(password_input, user_params)
            st.session_state.result = result
        except Exception as exc:
            st.error(f"Evaluation failed: {exc}")

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
if st.session_state.result:
    r = st.session_state.result
    st.divider()
    st.subheader("Evaluation Results")

    # Score and labels
    col_score, col_strength, col_verdict = st.columns(3)
    with col_score:
        st.metric("Score", f"{r['score']} / 10")
    with col_strength:
        st.metric("Strength", r["strength"])
    with col_verdict:
        if r["verdict"].lower() == "pass":
            st.metric("Verdict", "✅ Pass")
        else:
            st.metric("Verdict", "❌ Fail")

    # Score bar
    score_pct = r["score"] / 10
    if score_pct <= 0.3:
        bar_color = "🔴"
    elif score_pct <= 0.6:
        bar_color = "🟡"
    else:
        bar_color = "🟢"
    st.progress(score_pct, text=f"{bar_color} {r['score']}/10")

    # Explanation
    st.subheader("Why?")
    st.write(r["explanation"])

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.divider()
st.caption("Powered by Google Gemini · Grounded by secure_passwords.md")
