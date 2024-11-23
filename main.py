import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

from investor import InvestmentData, Investor
from loan_with_refinancing import LoanWithRefinancing

st.title("Kalkulacka refinancovani hypoteky")

#########################################
#                                       #
#           Mortgage calculation        #
#                                       #
#########################################

st.write("### Vstupni data - hypoteka")
col1, col2 = st.columns(2)
home_value = col1.number_input("Hypotecni pujcka", min_value=0, value=100_000)
old_interest_rate = col2.number_input("Urok [%]", min_value=0.1, value=5.0) / 100
old_loan_length = col1.number_input("Doba splaceni [roky]", min_value=1, value=30)
old_loan_current_year = col1.number_input("Rok refinancovani", min_value=1, max_value=old_loan_length - 1, value=1)
refinancing_interest_rate = col2.number_input("Urok refinancovani [%]", min_value=0.1, value=1.0) / 100
new_loan_length = col2.number_input("Doba refinancovani (v letech)", min_value=0, value=7)
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
    print(f"investment_values: {inst}")
    data.append({
        'number': inst.number,
        'payment': float(inst.payment),
        'interest': float(inst.interest),
        'principal': float(inst.principal),
        'total_interest': float(inst.total_interest),
        'balance': float(inst.balance),
        # "investment_values": float(inst.investment_values),
    })

df = pd.DataFrame(data)

df.drop(df.index[0], inplace=True)

overpayment_df = df[["total_interest", "balance"]]
payment_details_df = df[["interest", "principal"]]
others_df = df.groupby("payment")
# print(payment_details_df["principal"])

st.line_chart(overpayment_df)
st.line_chart(payment_details_df)
with st.expander("Zdrojova data"):
	st.table(df)
# st.line_chart(others_df)

#########################################
#                                       #
#           Alternative investment      #
#                                       #
#########################################

st.write("### Vstupni data - doplnkova investice")
col3, col4 = st.columns(2)
monthly_invest = col3.number_input("Mesicni investovana castka", min_value=0, value=1000)
yearly_interest_rate_safe = col4.number_input("Rocni urok - bezpecna varianta [%]", min_value=0.01, value=3.0) / 100
yearly_interest_rate_medium = col4.number_input("Rocni urok - stredni varianta [roky]", min_value=0.01, value=5.0) / 100
yearly_interest_rate_risky = col4.number_input("Rocni urok - riskantni varianta", min_value=0.01, value=8.0) / 100

invest_data = InvestmentData()
investor = Investor(
	invest_data=invest_data,
	monthly_invest=1000,
	yearly_interest_rates={
		"risky": 0.08, # add couple % to S&P?
		"medium": 0.05, # take from S&P index
		"safe": 0.03, # state bonds
	},
)
safe_values_df = invest_data.safe_values
medium_values_df = invest_data.medium_values
risky_values_df = invest_data.risky_values
print(safe_values_df)

st.line_chart(safe_values_df)
st.line_chart(medium_values_df)
st.line_chart(risky_values_df)
