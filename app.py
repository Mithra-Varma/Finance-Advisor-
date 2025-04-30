import streamlit as st
from auth import register_user, login_user
import pandas as pd
import altair as alt

st.set_page_config(page_title="AI Finance Advisor", page_icon="💸", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>AI Personal Finance Advisor</h1>
    <p style='text-align: center;'>Track your spending, visualize expenses, and improve savings smartly!</p>
""", unsafe_allow_html=True)

# Login/Register Section
if not st.session_state.logged_in:
    st.subheader("Login / Register")
    choice = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Email or Phone Number")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")
    else:
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful! Please log in.")
            else:
                st.warning("User already exists.")

# Main Finance Dashboard
if st.session_state.logged_in:
    st.markdown("---")
    st.subheader(f"Welcome, {username}")

    st.subheader("Enter Your Income and Expenses")

    income = st.number_input("Monthly Income (₹)", min_value=0.0)
    st.markdown("### Monthly Expenses:")
    categories = ["Rent", "Food", "Transportation", "Entertainment", "Others"]
    expenses = {cat: st.number_input(f"{cat} (₹)", min_value=0.0) for cat in categories}

    if st.button("Analyze"):
        df = pd.DataFrame(expenses.items(), columns=["Category", "Amount"])
        total_expense = df["Amount"].sum()
        savings = income - total_expense

        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:15px; border-radius:10px">
        <h4>Summary</h4>
        <b>Total Expenses:</b> ₹{total_expense}<br>
        <b>Estimated Savings:</b> ₹{savings}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Advice")
        if savings < 0:
            st.error("⚠️ You're spending more than you earn! Consider reducing your expenses.")
        elif savings < income * 0.2:
            st.warning("💡 Try to save at least 20% of your income.")
        else:
            st.success("✅ Great! Your savings are healthy.")

        st.subheader("Expense Distribution")
        chart = alt.Chart(df).mark_bar().encode(
            x="Category", y="Amount", color="Category"
        ).properties(width=600)
        st.altair_chart(chart)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
