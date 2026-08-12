import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="Finance Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================================================================
# CUSTOM CSS
# ==============================================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.dashboard-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 30px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.metric-title {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SAMPLE TRANSACTION DATA
# ==============================================================================

if "transactions" not in st.session_state:

    st.session_state.transactions = pd.DataFrame([
        {
            "ID": 1,
            "Date": "2026-08-01",
            "Description": "Monthly Salary",
            "Category": "Salary",
            "Type": "Income",
            "Amount": 75000
        },
        {
            "ID": 2,
            "Date": "2026-08-02",
            "Description": "Apartment Rent",
            "Category": "Housing",
            "Type": "Expense",
            "Amount": 18000
        },
        {
            "ID": 3,
            "Date": "2026-08-03",
            "Description": "Grocery Shopping",
            "Category": "Food",
            "Type": "Expense",
            "Amount": 4500
        },
        {
            "ID": 4,
            "Date": "2026-08-04",
            "Description": "Freelance Project",
            "Category": "Freelance",
            "Type": "Income",
            "Amount": 15000
        },
        {
            "ID": 5,
            "Date": "2026-08-05",
            "Description": "Electricity Bill",
            "Category": "Utilities",
            "Type": "Expense",
            "Amount": 2200
        },
        {
            "ID": 6,
            "Date": "2026-08-06",
            "Description": "Restaurant",
            "Category": "Food",
            "Type": "Expense",
            "Amount": 1200
        },
        {
            "ID": 7,
            "Date": "2026-08-07",
            "Description": "Uber",
            "Category": "Transport",
            "Type": "Expense",
            "Amount": 850
        },
        {
            "ID": 8,
            "Date": "2026-08-08",
            "Description": "Online Course",
            "Category": "Education",
            "Type": "Expense",
            "Amount": 3500
        }
    ])


# ==============================================================================
# SIDEBAR
# ==============================================================================

st.sidebar.title("💰 FinanceHub")
st.sidebar.caption("Personal Finance Analytics")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "💳 Transactions",
        "➕ Add Transaction",
        "📊 Analytics",
        "🎯 Budget",
        "⚙️ Settings"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Track your income, expenses and savings "
    "from one dashboard."
)


# ==============================================================================
# COMMON DATA
# ==============================================================================

transactions = st.session_state.transactions

income = transactions[
    transactions["Type"] == "Income"
]["Amount"].sum()

expenses = transactions[
    transactions["Type"] == "Expense"
]["Amount"].sum()

savings = income - expenses

savings_percentage = (
    (savings / income) * 100
    if income > 0
    else 0
)


# ==============================================================================
# DASHBOARD
# ==============================================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="dashboard-title">'
        'Personal Finance Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Monitor your financial activity and understand where your money goes.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------------------------
    # METRICS
    # --------------------------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    TOTAL INCOME
                </div>

                <div class="metric-value">
                    ₹{income:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    TOTAL EXPENSES
                </div>

                <div class="metric-value">
                    ₹{expenses:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    SAVINGS
                </div>

                <div class="metric-value">
                    ₹{savings:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    SAVINGS RATE
                </div>

                <div class="metric-value">
                    {savings_percentage:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Financial Overview'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)


    # Expense by Category
    with col1:

        expense_data = transactions[
            transactions["Type"] == "Expense"
        ]

        category_data = (
            expense_data
            .groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_data,
            x="Category",
            y="Amount",
            title="Expenses by Category"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Income vs Expenses
    with col2:

        comparison = pd.DataFrame({
            "Type": [
                "Income",
                "Expenses",
                "Savings"
            ],
            "Amount": [
                income,
                expenses,
                savings
            ]
        })

        fig = px.pie(
            comparison,
            names="Type",
            values="Amount",
            title="Income Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------------------------
    # RECENT TRANSACTIONS
    # --------------------------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Recent Transactions'
        '</div>',
        unsafe_allow_html=True
    )

    recent = transactions.tail(6).iloc[::-1]

    st.dataframe(
        recent,
        use_container_width=True,
        hide_index=True
    )


# ==============================================================================
# TRANSACTIONS
# ==============================================================================

elif page == "💳 Transactions":

    st.title("💳 Transactions")

    st.write(
        "Search and manage your financial transactions."
    )


    # --------------------------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(
            "🔍 Search",
            placeholder="Search description..."
        )

    with col2:

        type_filter = st.selectbox(
            "Transaction Type",
            [
                "All",
                "Income",
                "Expense"
            ]
        )

    with col3:

        categories = [
            "All"
        ] + sorted(
            transactions["Category"].unique().tolist()
        )

        category_filter = st.selectbox(
            "Category",
            categories
        )


    filtered = transactions.copy()


    if search:

        filtered = filtered[
            filtered["Description"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    if type_filter != "All":

        filtered = filtered[
            filtered["Type"] == type_filter
        ]


    if category_filter != "All":

        filtered = filtered[
            filtered["Category"] == category_filter
        ]


    st.divider()


    # --------------------------------------------------------------------------
    # TRANSACTION TABLE
    # --------------------------------------------------------------------------

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------------------------
    # DELETE
    # --------------------------------------------------------------------------

    st.subheader("🗑️ Delete Transaction")

    if len(transactions) > 0:

        delete_id = st.selectbox(
            "Select Transaction",
            transactions["ID"].tolist()
        )

        if st.button(
            "Delete Transaction",
            type="primary"
        ):

            st.session_state.transactions = (
                st.session_state.transactions[
                    st.session_state.transactions["ID"]
                    != delete_id
                ]
                .reset_index(drop=True)
            )

            st.success(
                "Transaction deleted successfully!"
            )

            st.rerun()


# ==============================================================================
# ADD TRANSACTION
# ==============================================================================

elif page == "➕ Add Transaction":

    st.title("➕ Add Transaction")

    st.write(
        "Record a new income or expense."
    )


    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            date = st.date_input(
                "Date",
                datetime.now()
            )

            description = st.text_input(
                "Description",
                placeholder="e.g. Grocery Shopping"
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0
            )

        with col2:

            transaction_type = st.selectbox(
                "Type",
                [
                    "Income",
                    "Expense"
                ]
            )

            category = st.selectbox(
                "Category",
                [
                    "Salary",
                    "Freelance",
                    "Business",
                    "Food",
                    "Housing",
                    "Transport",
                    "Utilities",
                    "Education",
                    "Entertainment",
                    "Shopping",
                    "Healthcare",
                    "Other"
                ]
            )


        submit = st.form_submit_button(
            "➕ Add Transaction"
        )


        if submit:

            if not description.strip():

                st.warning(
                    "Please enter a description."
                )

            elif amount <= 0:

                st.warning(
                    "Amount must be greater than zero."
                )

            else:

                new_id = (
                    st.session_state.transactions["ID"].max()
                    + 1
                    if len(st.session_state.transactions) > 0
                    else 1
                )

                new_transaction = pd.DataFrame([
                    {
                        "ID": new_id,
                        "Date": date.strftime("%Y-%m-%d"),
                        "Description": description,
                        "Category": category,
                        "Type": transaction_type,
                        "Amount": amount
                    }
                ])


                st.session_state.transactions = pd.concat(
                    [
                        st.session_state.transactions,
                        new_transaction
                    ],
                    ignore_index=True
                )


                st.success(
                    "Transaction added successfully!"
                )


# ==============================================================================
# ANALYTICS
# ==============================================================================

elif page == "📊 Analytics":

    st.title("📊 Financial Analytics")

    st.write(
        "Understand your financial behavior through interactive analytics."
    )


    # --------------------------------------------------------------------------
    # EXPENSE ANALYSIS
    # --------------------------------------------------------------------------

    expense_data = transactions[
        transactions["Type"] == "Expense"
    ]


    category_data = (
        expense_data
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )


    st.subheader("Expense Breakdown")


    fig = px.bar(
        category_data,
        x="Category",
        y="Amount",
        text="Amount",
        title="Where Your Money Goes"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------------------------
    # TRANSACTION TYPE
    # --------------------------------------------------------------------------

    st.subheader("Income vs Expenses")


    type_data = (
        transactions
        .groupby("Type")["Amount"]
        .sum()
        .reset_index()
    )


    fig = px.pie(
        type_data,
        names="Type",
        values="Amount",
        hole=0.45,
        title="Financial Distribution"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------------------------
    # TOP EXPENSES
    # --------------------------------------------------------------------------

    st.subheader("Top Expenses")


    top_expenses = (
        expense_data
        .sort_values(
            "Amount",
            ascending=False
        )
        .head(5)
    )


    st.dataframe(
        top_expenses,
        use_container_width=True,
        hide_index=True
    )


# ==============================================================================
# BUDGET
# ==============================================================================

elif page == "🎯 Budget":

    st.title("🎯 Monthly Budget")

    st.write(
        "Set your monthly spending target and monitor your progress."
    )


    budget = st.number_input(
        "Monthly Budget",
        min_value=0.0,
        value=30000.0,
        step=1000.0
    )


    current_expenses = expenses


    if budget > 0:

        percentage = (
            current_expenses / budget
        ) * 100

        percentage = min(
            percentage,
            100
        )

    else:

        percentage = 0


    st.subheader(
        f"₹{current_expenses:,.0f} / ₹{budget:,.0f}"
    )


    st.progress(
        percentage / 100
    )


    if current_expenses > budget:

        st.error(
            "⚠️ You have exceeded your monthly budget."
        )

    elif percentage >= 80:

        st.warning(
            "⚠️ You are close to your monthly budget."
        )

    else:

        st.success(
            "✓ You are within your monthly budget."
        )


    remaining = budget - current_expenses


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Budget",
            f"₹{budget:,.0f}"
        )


    with col2:

        st.metric(
            "Spent",
            f"₹{current_expenses:,.0f}"
        )


    with col3:

        st.metric(
            "Remaining",
            f"₹{remaining:,.0f}"
        )


# ==============================================================================
# SETTINGS
# ==============================================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")


    st.subheader("Dashboard Preferences")


    st.checkbox(
        "Show dashboard charts",
        value=True
    )


    st.checkbox(
        "Enable budget alerts",
        value=True
    )


    st.checkbox(
        "Show transaction notifications",
        value=True
    )


    st.divider()


    st.subheader("Database")


    st.write(
        f"Total transactions: "
        f"**{len(st.session_state.transactions)}**"
    )


    if st.button(
        "Reset Sample Data"
    ):

        del st.session_state.transactions

        st.success(
            "Sample data has been reset."
        )

        st.rerun()