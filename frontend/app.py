import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Knowledge Platform", page_icon="📚")
st.title("📚 AI Knowledge Platform")

# Store token and login state across reruns (Streamlit's way of "remembering" things)
if "token" not in st.session_state:
    st.session_state.token = None

# ---------- LOGIN / REGISTER SECTION ----------
if st.session_state.token is None:
    st.subheader("Login or Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            response = requests.post(f"{API_BASE}/login", json={"email": email, "password": password})
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with col2:
        if st.button("Register"):
            response = requests.post(f"{API_BASE}/register", json={"email": email, "password": password})
            if response.status_code == 200:
                st.success("Registered! Now click Login.")
            else:
                st.error(response.json().get("detail", "Registration failed"))

# ---------- MAIN APP (only shown after login) ----------
else:
    st.success("You are logged in!")

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.divider()
    st.subheader("💬 Ask a question about your documents")

    query = st.text_input("Your question")
    if st.button("Ask"):
        response = requests.get(f"{API_BASE}/chat", params={"query": query}, headers=headers)
        if response.status_code == 200:
            answer = response.json()["answer"]
            st.write("**Answer:**", answer)
        else:
            st.error(response.json().get("detail", "Something went wrong"))