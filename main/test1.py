import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def call_model(messages):
    response = requests.post(
        url=API_URL,
        timeout=30,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": MODEL, "messages": messages},
    )
    response_data = response.json()
    if "choices" not in response_data:
        st.error(f"خطا از سرور: {response_data}")
        return None
    return response_data["choices"][0]["message"]["content"]


# ---------- رابط کاربری ----------
st.title("📝 خلاصه‌ساز و پرسش‌گر متن")

user_text = st.text_area("متن خود را اینجا بچسبانید:", height=250)

# ---------- خلاصه ----------
if st.button("✨ خلاصه کن"):
    if not user_text.strip():
        st.warning("متنی وارد نشده.")
    else:
        with st.spinner("در حال خلاصه‌سازی..."):
            summary = call_model([
                {"role": "user", "content": f"Summarize this text:\n{user_text[:5000]}"}
            ])
        if summary:
            st.markdown("### خلاصه:")
            st.write(summary)

# ---------- پرسش‌وپاسخ ----------
st.markdown("---")
question = st.text_input("سوالت رو درباره‌ی متن بپرس:")

if st.button("💬 بپرس"):
    if not user_text.strip():
        st.warning("اول متن رو وارد کن.")
    elif not question.strip():
        st.warning("سوالت رو بنویس.")
    else:
        with st.spinner("در حال پاسخ..."):
            content = (
                "Based on the document below, answer the question.\n\n"
                f"Document:\n{user_text[:5000]}\n\n"
                f"Question: {question}"
            )
            answer = call_model([{"role": "user", "content": content}])
        if answer:
            st.markdown("### پاسخ:")
            st.write(answer)