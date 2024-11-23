import pandas as pd
import streamlit as st

from loan_with_refinancing import LoanWithRefinancing

st.title("Kalkulačka refinancování hypotéky")

#########################################
#                                       #
#           Mortgage calculation        #
#                                       #
#########################################

col1, col2 = st.columns(2)
home_value = col1.number_input("Původní splácená částka", min_value=0, value=100_000)
old_interest_rate = col2.number_input("Původní úrok [%]", min_value=0.1, value=2.0) / 100
old_loan_length = col1.number_input("Původní délka splácení [roky]", min_value=1, value=20)
old_loan_current_year = col1.number_input("Rok refinancování", min_value=1, max_value=old_loan_length - 1, value=5)
refinancing_interest_rate = col2.number_input("Úrok po refinancování [%]", min_value=0.1, value=5.0) / 100
new_loan_length = col2.number_input("Doba splácení hypotéky (v letech)", min_value=-20, value=25)
length_change = new_loan_length - old_loan_length

risk_choice = st.selectbox(
    "Kterou miru rizika pri investovani preferujete?",
    ("safe", "medium", "risky"),
)

loan = LoanWithRefinancing(
    principal=home_value,
    interest=old_interest_rate,
    term=old_loan_length,
    refinancing_year=old_loan_current_year,
    refinancing_interest=refinancing_interest_rate,
    new_hypo_length_change_years=length_change,
)
data = []
for inst in loan.schedule_with_refinancing():
    data.append(
        {
            "number": inst.number,
            "payment": float(inst.payment),
            "interest": float(inst.interest),
            "principal": float(inst.principal),
            "total_interest": float(inst.total_interest),
            "balance": float(inst.balance),
            "investment_values": float(inst.investment_values.get(risk_choice, 0)),
        }
    )

df = pd.DataFrame(data)

df.drop(df.index[0], inplace=True)

overpayment_df = df[["balance", "investment_values"]]
payment_details_df = df[["interest", "principal"]]
investment_data = df["investment_values"]

st.line_chart(overpayment_df, x = "Mesic", y = "Hodnota")
st.line_chart(payment_details_df)
with st.expander("Zdrojova data"):
    st.table(df)
