
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CashCompass AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 CashCompass AI")
st.subheader("Your Intelligent Financial Navigation Assistant")
st.write("Understand your spending, plan your budget, and prepare for future financial needs.")

st.divider()

st.header("1. Monthly Financial Details")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input(
        "Monthly income (₹)",
        min_value=0,
        value=30000,
        step=1000
    )

with col2:
    budget = st.number_input(
        "Monthly spending budget (₹)",
        min_value=0,
        value=20000,
        step=1000
    )

st.divider()

st.header("2. Add Your Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expense_form"):
    category = st.selectbox(
        "Expense category",
        ["Food", "Rent", "Travel", "Shopping", "Bills", "Education", "Healthcare", "Other"]
    )
    amount = st.number_input(
        "Expense amount (₹)",
        min_value=1,
        value=500,
        step=100
    )
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        st.session_state.expenses.append({
            "Category": category,
            "Amount": amount
        })
        st.success("Expense added successfully!")

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)

    total_expenses = int(df["Amount"].sum())
else:
    total_expenses = 0
    st.info("Add your expenses to see your financial summary.")

st.divider()

st.header("3. Financial Dashboard")

remaining = income - total_expenses
budget_remaining = budget - total_expenses

col1, col2, col3 = st.columns(3)

col1.metric("Monthly Income", f"₹{income:,.0f}")
col2.metric("Total Expenses", f"₹{total_expenses:,.0f}")
col3.metric("Remaining Balance", f"₹{remaining:,.0f}")

st.subheader("4. Smart Budget Insights")

if total_expenses > budget:
    st.error(f"You have exceeded your budget by ₹{total_expenses - budget:,.0f}.")
elif budget > 0:
    st.success(f"You have ₹{budget_remaining:,.0f} remaining in your budget.")
else:
    st.warning("Please enter a monthly spending budget.")

if remaining < 0:
    st.warning("Your expenses are higher than your income. Review your spending.")
elif income > 0:
    st.info(f"Your current balance is ₹{remaining:,.0f}.")

st.divider()

st.header("5. Simple Cash-Flow Forecast")

daily_average = total_expenses / 30
projected_expenses = daily_average * 30
projected_balance = income - projected_expenses

st.write(f"Estimated monthly expenses: ₹{projected_expenses:,.0f}")
st.write(f"Estimated remaining balance: ₹{projected_balance:,.0f}")

st.caption(
    "Forecasts are simple estimates based on expenses entered. "
    "They are not guaranteed predictions or professional financial advice."
)

st.divider()
st.caption("CashCompass AI | Navigate Money. Predict Tomorrow. Plan Better.")
