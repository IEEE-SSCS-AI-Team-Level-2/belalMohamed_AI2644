import streamlit as st
import pandas as pd

from src.services.bank_system import BankSystem, BankingError
from src.utils.csv_repository import CSVUserRepository, CSVTransactionRepository

st.set_page_config(
    page_title="EgyBank — Banking System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #790D5E;
        text-align: center;
        padding: 1rem 0;
    }
    .card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #790D5E;
        margin: 0.5rem 0;
    }
    .balance-big {
        font-size: 2rem;
        font-weight: 700;
        color: #0e9f6e;
    }
    .user-id-badge {
        background: #790D5E;
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .stAlert > div {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_bank_system() -> BankSystem:
    user_repo = CSVUserRepository(filepath="data/users.csv")
    txn_repo  = CSVTransactionRepository(filepath="data/transactions.csv")
    return BankSystem(user_repo=user_repo, transaction_repo=txn_repo)


bank = get_bank_system()

def show_success(message: str) -> None:
    st.success(f"✅ {message}")

def show_error(message: str) -> None:
    st.error(f"❌ {message}")

def show_user_card(user) -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card">
            <p style="color:#6b7280;margin:0">Account Holder</p>
            <h3 style="margin:0">{user.name}</h3>
            <span class="user-id-badge">{user.user_id}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <p style="color:#6b7280;margin:0">Current Balance</p>
            <div class="balance-big">{user.balance:,.2f} EGP</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card">
            <p style="color:#6b7280;margin:0">Phone Number</p>
            <h3 style="margin:0">{user.phone}</h3>
            <small style="color:#6b7280">Member since {user.created_at[:10]}</small>
        </div>
        """, unsafe_allow_html=True)


st.sidebar.markdown("## 🏦 EGYBank")
st.sidebar.markdown("---")

pages = {
    "🏠 Home / Dashboard":      "home",
    "➕ Create Account":         "create",
    "🔍 View Account":           "view",
    "💰 Deposit / Withdraw":    "transactions",
    "✏️  Update Account":         "update",
    "🗑️  Delete Account":         "delete",
    "📜 Transaction History":    "history",
    "👥 All Users (Admin)":      "admin",
}

selected_label = st.sidebar.radio("Navigation", list(pages.keys()))
page = pages[selected_label]

st.sidebar.markdown("---")


# Home / Dashboard
if page == "home":
    st.markdown('<div class="main-header">🏦 EGYBank</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#6b7280'>Your trusted digital banking system</p>", unsafe_allow_html=True)
    st.markdown("---")

    all_users = bank.get_all_users()
    all_txns  = bank.get_all_transactions()

    col1, col2, col3 = st.columns(3)
    col1.metric("👤 Total Accounts", len(all_users))
    col2.metric("📊 Total Transactions", len(all_txns))
    total_assets = sum(u.balance for u in all_users)
    col3.metric("💵 Total Assets Under Management", f"{total_assets:,.2f} EGP")

    if all_txns:
        st.markdown("### 🕐 Recent Activity")
        recent = all_txns[:5]
        df = pd.DataFrame([t.to_dict() for t in recent])[
            ["timestamp", "user_id", "transaction_type", "amount", "balance_after", "description"]
        ]
        df.columns = ["Time", "User ID", "Type", "Amount (EGP)", "Balance After", "Description"]
        st.dataframe(df, use_container_width=True, hide_index=True)


# Create Account
elif page == "create":
    st.header("➕ Open a New Account")
    st.markdown("Fill in the details below to create your bank account.")

    with st.form("create_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name    = st.text_input("Full Name", placeholder="e.g. Ahmed Hassan")
            phone   = st.text_input("Phone Number", placeholder="e.g. 01012345678")
        with col2:
            password  = st.text_input("Password (min 6 chars)", type="password")
            password2 = st.text_input("Confirm Password", type="password")

        initial_balance = st.number_input(
            "Initial Deposit (EGP)", min_value=0.0, value=0.0, step=100.0
        )
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if password != password2:
            show_error("Passwords do not match.")
        else:
            try:
                user = bank.create_account(name, password, phone, initial_balance)
                show_success(f"Account created! Your User ID is **{user.user_id}** — save it!")
                show_user_card(user)
            except BankingError as e:
                show_error(str(e))


# View Account
elif page == "view":
    st.header("🔍 View Account")

    user_id = st.text_input("Enter User ID", placeholder="e.g. USR-0001").strip().upper()
    if st.button("Fetch Account", use_container_width=True):
        if not user_id:
            show_error("Please enter a User ID.")
        else:
            try:
                user = bank.get_user(user_id)
                show_user_card(user)
            except BankingError as e:
                show_error(str(e))


# Deposit & Withdrawal
elif page == "transactions":
    st.header("💰 Deposit & Withdrawal")

    user_id = st.text_input("User ID", placeholder="e.g. USR-0001").strip().upper()
    operation = st.radio("Operation", ["Deposit", "Withdraw"], horizontal=True)
    amount = st.number_input("Amount (EGP)", min_value=0.01, value=100.0, step=50.0)

    if st.button("Confirm Transaction", use_container_width=True):
        if not user_id:
            show_error("Please enter a User ID.")
        else:
            try:
                if "Deposit" in operation:
                    user = bank.deposit(user_id, amount)
                    show_success(f"Deposited **{amount:,.2f} EGP**. New balance: **{user.balance:,.2f} EGP**")
                else:
                    user = bank.withdraw(user_id, amount)
                    show_success(f"Withdrew **{amount:,.2f} EGP**. New balance: **{user.balance:,.2f} EGP**")
                show_user_card(user)
            except BankingError as e:
                show_error(str(e))


# Update Account Information
elif page == "update":
    st.header("✏️ Update Account Information")

    user_id = st.text_input("User ID", placeholder="e.g. USR-0001").strip().upper()
    update_type = st.selectbox(
        "What would you like to update?",
        ["Name", "Phone Number", "Password"]
    )

    st.markdown("---")

    if update_type == "Name":
        new_name = st.text_input("New Full Name")
        if st.button("Save Name", use_container_width=True):
            try:
                user = bank.update_name(user_id, new_name)
                show_success(f"Name updated to **{user.name}**.")
            except BankingError as e:
                show_error(str(e))

    elif update_type == "Phone Number":
        new_phone = st.text_input("New Phone Number")
        if st.button("Save Phone", use_container_width=True):
            try:
                user = bank.update_phone(user_id, new_phone)
                show_success(f"Phone updated to **{user.phone}**.")
            except BankingError as e:
                show_error(str(e))

    elif update_type == "Password":
        old_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password (min 6 chars)", type="password")
        new_pw2 = st.text_input("Confirm New Password", type="password")
        if st.button("Save Password", use_container_width=True):
            if new_pw != new_pw2:
                show_error("New passwords do not match.")
            else:
                try:
                    bank.update_password(user_id, old_pw, new_pw)
                    show_success("Password updated successfully.")
                except BankingError as e:
                    show_error(str(e))


# Delete Account
elif page == "delete":
    st.header("🗑️ Delete Account")
    st.warning("⚠️ This action is irreversible. All data will be permanently deleted.")

    user_id  = st.text_input("User ID", placeholder="e.g. USR-0001").strip().upper()
    password = st.text_input("Confirm Password", type="password")

    confirm = st.checkbox("I understand this cannot be undone")
    if st.button("Delete Account", use_container_width=True, type="primary"):
        if not confirm:
            show_error("Please check the confirmation box.")
        elif not user_id:
            show_error("Please enter a User ID.")
        else:
            try:
                bank.delete_account(user_id, password)
                show_success(f"Account **{user_id}** has been permanently deleted.")
            except BankingError as e:
                show_error(str(e))


# Transaction History
elif page == "history":
    st.header("📜 Transaction History")

    user_id = st.text_input("User ID", placeholder="e.g. USR-0001").strip().upper()
    if st.button("Load History", use_container_width=True):
        if not user_id:
            show_error("Please enter a User ID.")
        else:
            try:
                user = bank.get_user(user_id)
                txns = bank.get_transaction_history(user_id)

                st.markdown(f"### Transactions for {user.name} ({user_id})")
                st.markdown(f"**Current Balance:** {user.balance:,.2f} EGP")
                st.markdown(f"**Total Transactions:** {len(txns)}")
                st.markdown("---")

                if not txns:
                    st.info("No transactions found for this account.")
                else:
                    df = pd.DataFrame([t.to_dict() for t in txns])[
                        ["timestamp", "transaction_type", "amount", "balance_after", "description"]
                    ]
                    df.columns = ["Date & Time", "Type", "Amount (EGP)", "Balance After (EGP)", "Description"]
                    st.dataframe(df, use_container_width=True, hide_index=True)

            except BankingError as e:
                show_error(str(e))


# All Accounts
elif page == "admin":
    st.header("👥 All Accounts — Admin View")

    all_users = bank.get_all_users()

    if not all_users:
        st.info("No accounts exist yet. Create one first!")
    else:
        data = [
            {
                "User ID":    u.user_id,
                "Name":       u.name,
                "Phone":      u.phone,
                "Balance (EGP)": f"{u.balance:,.2f}",
                "Created At": u.created_at,
            }
            for u in all_users
        ]
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📊 Balance Distribution")
        balances = {u.name: u.balance for u in all_users}
        if balances:
            st.bar_chart(balances)
