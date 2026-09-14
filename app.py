import streamlit as st  
from bank import Bank


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Banking System",
    page_icon="🏦",
    layout="wide"
)


# --------------------------------
# Initialize bank
# --------------------------------

bank = Bank()


# --------------------------------
# CSS
# --------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# Header
# --------------------------------

st.markdown(
    '<div class="main-title">🏦 Banking Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Simple Python + Streamlit Banking Application</div>',
    unsafe_allow_html=True
)


# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.title("🏦 Banking System")

menu = st.sidebar.radio(
    "Choose an operation",
    [
        "🏠 Dashboard",
        "➕ Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "🔎 Account Details",
        "✏️ Update Account",
        "🗑️ Delete Account"
    ]
)


# =========================================
# DASHBOARD
# =========================================

if menu == "🏠 Dashboard":

    stats = bank.get_statistics()

    st.subheader("Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Accounts",
            stats["total_accounts"]
        )

    with col2:
        st.metric(
            "Total Bank Balance",
            f"₹{stats['total_balance']:,.2f}"
        )

    st.divider()

    st.info(
        """
        Welcome to the Banking Management System.

        Use the sidebar to:

        - Create a new account
        - Deposit money
        - Withdraw money
        - View account details
        - Update account information
        - Delete an account
        """
    )


# =========================================
# CREATE ACCOUNT
# =========================================

elif menu == "➕ Create Account":

    st.subheader("Create New Account")

    with st.form("create_account_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input("Email Address")

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

    if submitted:

        if pin != confirm_pin:

            st.error("PINs do not match.")

        else:

            success, result = bank.create_account(
                name,
                age,
                email,
                pin
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

                st.info(
                    f"Your account number is: **{result}**"
                )

                st.warning(
                    "Please save your account number. "
                    "You will need it for future transactions."
                )

            else:

                st.error(result)


# =========================================
# DEPOSIT
# =========================================

elif menu == "💰 Deposit":

    st.subheader("Deposit Money")

    with st.form("deposit_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            max_value=10000.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Deposit"
        )

    if submitted:

        success, result = bank.deposit(
            account_number.strip().upper(),
            pin,
            amount
        )

        if success:

            st.success(
                "Money deposited successfully!"
            )

            st.metric(
                "New Balance",
                f"₹{result:,.2f}"
            )

        else:

            st.error(result)


# =========================================
# WITHDRAW
# =========================================

elif menu == "💸 Withdraw":

    st.subheader("Withdraw Money")

    with st.form("withdraw_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "Withdraw"
        )

    if submitted:

        success, result = bank.withdraw(
            account_number.strip().upper(),
            pin,
            amount
        )

        if success:

            st.success(
                "Money withdrawn successfully!"
            )

            st.metric(
                "New Balance",
                f"₹{result:,.2f}"
            )

        else:

            st.error(result)


# =========================================
# ACCOUNT DETAILS
# =========================================

elif menu == "🔎 Account Details":

    st.subheader("Account Details")

    with st.form("account_details_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "View Account"
        )

    if submitted:

        account = bank.get_account(
            account_number.strip().upper(),
            pin
        )

        if account:

            st.success("Account found!")

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Personal Information")

                st.write(
                    f"**Name:** {account['name']}"
                )

                st.write(
                    f"**Age:** {account['age']}"
                )

                st.write(
                    f"**Email:** {account['email']}"
                )

                st.write(
                    f"**Account Number:** "
                    f"{account['account_number']}"
                )

            with col2:

                st.write("### Account Information")

                st.metric(
                    "Current Balance",
                    f"₹{account['balance']:,.2f}"
                )

            st.divider()

            st.write("### Transaction History")

            transactions = account.get(
                "transactions",
                []
            )

            if transactions:

                for transaction in reversed(transactions):

                    if transaction["type"] == "Deposit":
                        icon = "🟢"

                    elif transaction["type"] == "Withdrawal":
                        icon = "🔴"

                    else:
                        icon = "🔵"

                    st.write(
                        f"{icon} **{transaction['type']}** — "
                        f"₹{transaction['amount']:,.2f} — "
                        f"{transaction['date']}"
                    )

        else:

            st.error(
                "Invalid account number or PIN."
            )


# =========================================
# UPDATE ACCOUNT
# =========================================

elif menu == "✏️ Update Account":

    st.subheader("Update Account")

    with st.form("update_account_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4
        )

        st.write("Leave a field empty if you don't want to change it.")

        new_name = st.text_input(
            "New Name"
        )

        new_email = st.text_input(
            "New Email"
        )

        new_pin = st.text_input(
            "New PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Update Account"
        )

    if submitted:

        success, message = bank.update_account(
            account_number.strip().upper(),
            pin,
            new_name,
            new_email,
            new_pin
        )

        if success:

            st.success(message)

        else:

            st.error(message)


# =========================================
# DELETE ACCOUNT
# =========================================

elif menu == "🗑️ Delete Account":

    st.subheader("Delete Account")

    st.warning(
        "⚠️ This action cannot be undone."
    )

    with st.form("delete_account_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        confirmation = st.checkbox(
            "I understand that my account will be deleted."
        )

        submitted = st.form_submit_button(
            "Delete Account"
        )

    if submitted:

        if not confirmation:

            st.error(
                "Please confirm account deletion."
            )

        else:

            success, message = bank.delete_account(
                account_number.strip().upper(),
                pin
            )

            if success:

                st.success(message)

            else:

                st.error(message)