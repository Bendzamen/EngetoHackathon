import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Kalkulacka refinancovani hypoteky")

st.write("### Vstupni data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Splacena castka", min_value=0, value=500000)
deposit = col1.number_input("Zbyva doplatit", min_value=0, max_value=home_value, value=100000)
interest_rate = col2.number_input("Urok (in %)", min_value=0.1, value=5.5)
loan_term = col1.number_input("Doba splaceni (in years)", min_value=1, value=30)
current_year = col1.number_input("Rok splaceni", min_value=1, value=30)
refinancing_interest_rate = col2.number_input("Urok refinancovani (in %)", min_value=0.1, value=2.5)
new_loan_length = col2.number_input("Doba refinancovani (in years)", min_value=1, value=30)

# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Mesicni splatky", value=f"${monthly_payment:,.2f}")
col2.metric(label="Splatky celkem", value=f"${total_payments:,.0f}")
col3.metric(label="Urok celkem", value=f"${total_interest:,.0f}")


# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
            
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart.
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
print(payments_df)
st.line_chart(payments_df)
