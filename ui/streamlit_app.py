import streamlit as st
import requests

st.set_page_config(page_title="Enterprise RAG Demo", layout="wide")
st.title("Enterprise RAG Intelligence Challenge - Free Version")

role = st.selectbox("Role", ["HR", "Finance", "Security", "Manager"])
default_user = {
    "HR": "u_hr_1",
    "Finance": "u_fin_1",
    "Security": "u_sec_1",
    "Manager": "u_mgr_1"
}[role]

user_id = st.text_input("User ID", default_user)
question = st.text_area("Ask your question", height=120)

if st.button("Submit Query"):
    payload = {"user_id": user_id, "role": role, "question": question}
    response = requests.post("http://localhost:8000/query", json=payload, timeout=120)

    if response.status_code == 200:
        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Confidence", data["confidence"])
        with col2:
            st.metric("Denied", str(data["denied"]))

        st.subheader("Citations")
        for c in data["citations"]:
            st.write("-", c)

        st.subheader("Retrieved Evidence")
        for chunk in data["retrieved_chunks"]:
            with st.expander(f"{chunk['title']} | score={chunk['score']}"):
                st.write(chunk["text"])
                st.caption(chunk["citation"])
    else:
        st.error("API request failed.")