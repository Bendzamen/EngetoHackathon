import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

from loan_with_refinancing import LoanWithRefinancing

st.title("Kalkulacka refinancovani hypoteky")

st.write("### Vstupni data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Splacena castka", min_value=0, value=100_000)
deposit = col1.number_input("Zbyva doplatit", min_value=0, max_value=home_value, value=80_000)
old_interest_rate = col2.number_input("Urok (in %)", min_value=0.1, value=2.0) / 100
old_loan_length = col1.number_input("Doba splaceni (in years)", min_value=1, value=30)
old_loan_current_year = col1.number_input("Rok splaceni", min_value=1, value=1)
refinancing_interest_rate = col2.number_input("Urok refinancovani (in %)", min_value=0.1, value=1.0) / 100
new_loan_length = col2.number_input("Doba refinancovani (in years)", min_value=0.0, value=7.0)
length_change = old_loan_length - new_loan_length


loan = LoanWithRefinancing(
    principal = home_value,
        interest = old_interest_rate,
        term = old_loan_length,
        refinancing_year = old_loan_current_year,
        refinancing_interest = refinancing_interest_rate,
        new_hypo_length_change_years = length_change,
)
data = []
for inst in loan.schedule():
    data.append({
        'number': inst.number,
        'payment': float(inst.payment),
        'interest': float(inst.interest),
        'principal': float(inst.principal),
        'total_interest': float(inst.total_interest),
        'balance': float(inst.balance)
    })

df = pd.DataFrame(data)

df.drop(df.index[0], inplace=True)

overpayment_df = df[["total_interest", "balance"]]
payment_details_df = df[["interest", "principal"]]
others_df = df.groupby("payment")
print(payment_details_df["principal"])

st.line_chart(overpayment_df)
st.line_chart(payment_details_df)
with st.expander("Zdrojova data"):
	st.table(df)
# st.line_chart(others_df)
