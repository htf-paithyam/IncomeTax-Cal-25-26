import streamlit as st
import pandas as pd

def calculate_old_regime(income, deductions):
    """Calculate tax under old regime with standard deduction"""
    # Apply standard deduction of 50,000
    standard_deduction = 50000
    taxable_income = income - standard_deduction - deductions

    tax = 0
    breakdown = []

    slabs = [
        (0, 250000, 0),
        (250000, 500000, 0.05),
        (500000, 1000000, 0.20),
        (1000000, float('inf'), 0.30)
    ]

    remaining_income = taxable_income
    for lower, upper, rate in slabs:
        if remaining_income > lower:
            taxable_in_slab = min(remaining_income - lower, upper - lower) if upper != float('inf') else remaining_income - lower
            tax_in_slab = taxable_in_slab * rate
            tax += tax_in_slab
            if tax_in_slab > 0:
                breakdown.append({
                    'Slab': f"₹{lower:,} to ₹{upper:,}" if upper != float('inf') else f"Above ₹{lower:,}",
                    'Amount': f"₹{taxable_in_slab:,.0f}",
                    'Rate': f"{rate*100:.0f}%",
                    'Tax': f"₹{tax_in_slab:,.0f}"
                })

    cess = tax * 0.04
    return tax, cess, breakdown, taxable_income

def calculate_new_regime(income):
    """Calculate tax under new regime with standard deduction"""
    # Apply standard deduction of 75,000
    standard_deduction = 75000
    taxable_income = income - standard_deduction

    tax = 0
    breakdown = []

    slabs = [
        (0, 400000, 0),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, float('inf'), 0.30)
    ]

    remaining_income = taxable_income
    for lower, upper, rate in slabs:
        if remaining_income > lower:
            taxable_in_slab = min(remaining_income - lower, upper - lower) if upper != float('inf') else remaining_income - lower
            tax_in_slab = taxable_in_slab * rate
            tax += tax_in_slab
            if tax_in_slab > 0:
                breakdown.append({
                    'Slab': f"₹{lower:,} to ₹{upper:,}" if upper != float('inf') else f"Above ₹{lower:,}",
                    'Amount': f"₹{taxable_in_slab:,.0f}",
                    'Rate': f"{rate*100:.0f}%",
                    'Tax': f"₹{tax_in_slab:,.0f}"
                })

    # Apply rebate of ₹60,000
    if tax <= 60000:
        tax = 0
        breakdown.append({
            'Slab': 'Tax Rebate Applied',
            'Amount': '-',
            'Rate': '-',
            'Tax': '₹0'
        })

    cess = tax * 0.04
    return tax, cess, breakdown, taxable_income

def main():
    # Set page config for better mobile display
    st.set_page_config(page_title="Income Tax Calculator FY 2025-26", layout="wide", initial_sidebar_state="collapsed")

    # Custom CSS for better mobile responsiveness
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        @media (max-width: 768px) {
            .stColumn {
                min-width: 100%;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("Income Tax Calculator FY 2025-26")

    # Input Section
    col1, col2 = st.columns([2, 2])

    with col1:
        income = st.number_input("Enter Annual Income (₹)", min_value=0, value=0, step=10000, format="%d")

    with col2:
        deductions = st.number_input("Enter Total Deductions (₹)", min_value=0, value=0, step=1000, format="%d",
                                   help="Applicable only for Old Regime (80C, 80D, HRA, etc.)")

    # Calculate taxes
    old_tax, old_cess, old_breakdown, old_taxable = calculate_old_regime(income, deductions)
    new_tax, new_cess, new_breakdown, new_taxable = calculate_new_regime(income)

    # Display Results
    st.markdown("### Tax Calculation Results")

    col1, col2 = st.columns(2)

    # Old Regime Results
    with col1:
        st.info("#### Old Regime")
        st.write(f"Gross Income: ₹{income:,}")
        st.write(f"Standard Deduction: ₹50,000")
        st.write(f"Other Deductions: ₹{deductions:,}")
        st.write(f"Taxable Income: ₹{old_taxable:,}")

        st.write("Tax Breakdown:")
        if old_breakdown:
            df_old = pd.DataFrame(old_breakdown)
            st.table(df_old)

        st.write(f"Health & Education Cess (4%): ₹{old_cess:,.0f}")
        st.markdown(f"Total Tax: ₹{(old_tax + old_cess):,.0f}")

    # New Regime Results
    with col2:
        st.success("#### New Regime")
        st.write(f"Gross Income: ₹{income:,}")
        st.write(f"Standard Deduction: ₹75,000")
        st.write(f"Taxable Income: ₹{new_taxable:,}")

        st.write("Tax Breakdown:")
        if new_breakdown:
            df_new = pd.DataFrame(new_breakdown)
            st.table(df_new)

        st.write(f"Health & Education Cess (4%): ₹{new_cess:,.0f}")
        st.markdown(f"Total Tax: ₹{(new_tax + new_cess):,.0f}")

    # Recommendation
    st.markdown("### Recommendation")
    old_total = old_tax + old_cess
    new_total = new_tax + new_cess
    if old_total < new_total:
        st.success(f"Old Regime is better for you! You save ₹{new_total - old_total:,.0f}")
    elif new_total < old_total:
        st.success(f"New Regime is better for you! You save ₹{old_total - new_total:,.0f}")
    else:
        st.info("Both regimes result in the same tax amount.")

    # Notes
    st.markdown("### Notes")
    st.markdown("""
    - Old Regime: Standard deduction of ₹50,000 + Additional deductions available
    - New Regime: Standard deduction of ₹75,000 (No other deductions available)
    - Tax rebate of ₹60,000 available in New Regime
    - 4% Health & Education Cess applicable on tax amount in both regimes
    """)

if __name__ == "__main__":
    main()