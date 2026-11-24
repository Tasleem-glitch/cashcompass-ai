import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CashCompass AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 CashCompass AI")
st.subheader("Your Intelligent Financial Navigation Assistant")
st.write("Track spending, monitor budgets and make smarter financial decisions.")

st.divider()

st.header("1. Monthly Financial Details")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input(
        "Monthly income (₹)", min_value=0,
        value=30000, step=1000
    )

with col2:
    budget = st.number_input(
        "Monthly spending budget (₹)", min_value=0,
        value=20000, step=1000
    )

st.divider()

st.header("2. Expense Management")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expense_form"):
    category = st.selectbox(
        "Expense category",
        ["Food", "Rent", "Travel", "Shopping",
         "Bills", "Education", "Healthcare", "Other"]
    )

    amount = st.number_input(
        "Expense amount (₹)",
        min_value=1, value=500, step=100
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
    total_expenses = int(df["Amount"].sum())

    st.subheader("Your Expense Records")
    st.dataframe(df, use_container_width=True)

    if st.button("Clear All Expenses"):
        st.session_state.expenses = []
        st.rerun()
else:
    df = pd.DataFrame(columns=["Category", "Amount"])
    total_expenses = 0
    st.info("Add expenses to view your analysis.")

st.divider()

st.header("3. Financial Dashboard")

remaining = income - total_expenses
budget_remaining = budget - total_expenses

col1, col2, col3 = st.columns(3)

col1.metric("Monthly Income", f"₹{income:,.0f}")
col2.metric("Total Expenses", f"₹{total_expenses:,.0f}")
col3.metric("Remaining Balance", f"₹{remaining:,.0f}")

st.divider()

st.header("4. Spending Category Analysis")

if not df.empty:
    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_totals)

    st.subheader("Category-wise Spending")

    for name, value in category_totals.items():
        st.write(f"**{name}:** ₹{value:,.0f}")
else:
    st.info("Your category chart will appear after adding expenses.")

st.divider()

st.header("5. Smart Budget Insights")

if budget > 0:
    budget_used = total_expenses / budget

    st.progress(min(budget_used, 1.0))

    st.write(f"Budget used: {budget_used * 100:.1f}%")

    if total_expenses > budget:
        st.error(
            f"Budget exceeded by ₹{total_expenses - budget:,.0f}."
        )
    else:
        st.success(
            f"Budget remaining: ₹{budget_remaining:,.0f}"
        )
else:
    st.warning("Enter a budget to receive budget insights.")

if remaining < 0:
    st.error("Your expenses are higher than your income.")
elif income > 0:
    st.info(f"Your remaining income is ₹{remaining:,.0f}.")

st.divider()

st.header("6. Smart Saving Suggestions")

if total_expenses == 0:
    st.info("Add expenses to receive saving suggestions.")
elif remaining > 0:
    suggested_saving = remaining * 0.20
    st.success(
        f"Consider setting aside ₹{suggested_saving:,.0f} "
        "as a possible savings target."
    )
else:
    st.warning(
        "Review non-essential spending and prioritize necessary expenses."
    )

st.divider()

st.header("7. Cash-Flow Summary")

st.write(f"Income: ₹{income:,.0f}")
st.write(f"Recorded expenses: ₹{total_expenses:,.0f}")
st.write(f"Estimated balance: ₹{remaining:,.0f}")

st.caption(
    "Calculations use the information entered by the user. "
    "Savings suggestions are illustrative, not financial advice. "
    "Expense records are stored only during the active app session."
)

st.divider()

st.caption(
    "CashCompass AI | Navigate Money. Predict Tomorrow. Plan Better."
)

