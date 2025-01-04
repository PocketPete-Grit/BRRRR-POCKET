
import streamlit as st

# Display Logo
st.image("PP_Logo_Transparent.png", width=200)  # Adjust the width if needed

# App Title
st.title("BRRRR (Buy, Rehab, Rent, Refinance, Repeat) Calculator")

# Input Fields
st.header("Property Details")
purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=1000.0, format="%.2f")
rehab_costs = st.number_input("Rehab Costs ($)", min_value=0.0, step=1000.0, format="%.2f")
arv = st.number_input("After Repair Value (ARV) ($)", min_value=0.0, step=1000.0, format="%.2f")

st.header("Loan Terms for Refinance")
ltv = st.slider("Loan-to-Value (LTV) %", min_value=50, max_value=100, step=1, value=75)  # Default 75% LTV
interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1, format="%.2f", value=5.0)
loan_term = st.number_input("Loan Term (years)", min_value=1, step=1, value=30)

st.header("Rental Details")
monthly_rent = st.number_input("Monthly Rental Income ($)", min_value=0.0, step=100.0, format="%.2f")
taxes = st.number_input("Monthly Taxes ($)", min_value=0.0, step=100.0, format="%.2f")
insurance = st.number_input("Monthly Insurance ($)", min_value=0.0, step=50.0, format="%.2f")
property_management = st.number_input("Monthly Property Management ($)", min_value=0.0, step=50.0, format="%.2f")
other_expenses = st.number_input("Other Monthly Expenses ($)", min_value=0.0, step=50.0, format="%.2f")

st.header("CapEx, Maintenance, and Vacancy")
capex_percentage = st.slider("CapEx (% of Rent)", min_value=0, max_value=20, step=1, value=5)  # Default 5%
maintenance_percentage = st.slider("Maintenance (% of Rent)", min_value=0, max_value=20, step=1, value=5)  # Default 5%
vacancy_percentage = st.slider("Vacancy (% of Rent)", min_value=0, max_value=20, step=1, value=5)  # Default 5%

# Calculations
# Refinance Amount
refinance_amount = arv * (ltv / 100)

# Monthly Mortgage Payment
monthly_interest_rate = (interest_rate / 100) / 12
loan_term_months = loan_term * 12
if monthly_interest_rate > 0:
    mortgage_payment = refinance_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) /         ((1 + monthly_interest_rate) ** loan_term_months - 1)
else:
    mortgage_payment = refinance_amount / loan_term_months

# CapEx, Maintenance, and Vacancy Costs
capex = monthly_rent * (capex_percentage / 100)
maintenance = monthly_rent * (maintenance_percentage / 100)
vacancy = monthly_rent * (vacancy_percentage / 100)

# Total Operating Expenses
total_expenses = taxes + insurance + property_management + other_expenses + mortgage_payment + capex + maintenance + vacancy

# Cash Flow
cash_flow = monthly_rent - total_expenses

# Total Investment (Purchase Price + Rehab Costs - Refinance Amount)
total_investment = purchase_price + rehab_costs - refinance_amount

# Cash-on-Cash ROI
if total_investment > 0:
    cash_on_cash_roi = (cash_flow * 12 / total_investment) * 100
else:
    cash_on_cash_roi = 0

# Equity Check
equity = arv - refinance_amount
equity_percentage = (equity / arv) * 100 if arv > 0 else 0

# Good BRRRR Metric
is_good_brrrr = equity_percentage >= 15 and cash_on_cash_roi >= 15

# Display Results
st.header("Results")
st.write(f"**Refinance Amount:** ${refinance_amount:,.2f}")
st.write(f"**Monthly Mortgage Payment:** ${mortgage_payment:,.2f}")
st.write(f"**CapEx Cost (Monthly):** ${capex:,.2f}")
st.write(f"**Maintenance Cost (Monthly):** ${maintenance:,.2f}")
st.write(f"**Vacancy Cost (Monthly):** ${vacancy:,.2f}")
st.write(f"**Total Monthly Operating Expenses:** ${total_expenses:,.2f}")
st.write(f"**Monthly Cash Flow:** ${cash_flow:,.2f}")
st.write(f"**Total Investment After Refinance:** ${total_investment:,.2f}")
st.write(f"**Cash-on-Cash ROI:** {cash_on_cash_roi:.2f}%")
st.write(f"**Equity Percentage:** {equity_percentage:.2f}%")

# Good BRRRR Decision
st.header("Good BRRRR?")
if is_good_brrrr:
    st.success("This is a GOOD BRRRR! 🎉")
else:
    st.error("This is NOT a good BRRRR.")
