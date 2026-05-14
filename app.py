import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from auth import register_user, login_user
from backend import (
    categorize_transaction,
    generate_insights,
)
from db import (
    add_transaction,
    get_transactions
)

# PAGE CONFIG
st.set_page_config(
    page_title="Expense Agent Pro",
    page_icon="logo.png",
    layout="centered"
)

# LOGO
logo = Image.open("logo.jpeg")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(logo, width=220)

# TITLE
st.title("💰 Expense Agent Pro")
st.caption("An AI Agent That Thinks Before You Spend")

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# SIDEBAR MENU
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

# REGISTER
if menu == "Register":

    st.subheader("📝 Create Account")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        try:
            register_user(username, password)
            st.success("✅ Account Created Successfully")

        except:
            st.error("⚠️ Username already exists")

# LOGIN
elif menu == "Login":

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if login_user(username, password):
            st.session_state.user = username
            st.success("✅ Login Successful")

        else:
            st.error("❌ Invalid Username or Password")

# MAIN APPLICATION
if st.session_state.user:

    st.sidebar.success(
        f"Logged in as {st.session_state.user}"
    )

    st.header("📊 Dashboard")

    # ADD TRANSACTION
    st.sidebar.header("➕ Add Transaction")

    transaction_name = st.sidebar.text_input(
        "Transaction Name"
    )

    transaction_amount = st.sidebar.number_input(
        "Amount",
        min_value=0
    )

    if st.sidebar.button("Add Transaction"):

        category = categorize_transaction(
            transaction_name
        )

        add_transaction(
            st.session_state.user,
            transaction_name,
            transaction_amount,
            category
        )

        st.sidebar.success("Transaction Added")

    # FETCH DATA
    data = get_transactions(
        st.session_state.user
    )

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Name",
                "Amount",
                "Category"
            ]
        )

        # TABLE
        st.subheader("📄 Transactions")
        st.dataframe(
            df,
            use_container_width=True
        )

        # CHART
        st.subheader("📈 Spending Breakdown")

        chart_data = df.groupby(
            "Category"
        )["Amount"].sum()

        fig, ax = plt.subplots()

        chart_data.plot(
            kind="bar",
            ax=ax
        )

        st.pyplot(fig)

        # INSIGHTS
        st.subheader("🧠 AI Insights")

        insights = generate_insights(data)

        for insight in insights:
            st.info(insight)